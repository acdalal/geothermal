import time
from .boreholes import boreholes
from django.db import connections
from datetime import timedelta, datetime
from .createQueries import (
    createEntireDataOutageQuery,
    createTempProfileQueryByDay,
    createTempProfileQueryByMeasurement,
    # createTempVsDepthQuery,
    createTempVsTimeQuery,
)
from .constants import HOURS, METRIC, IMPERIAL
import re


def _toFarenheit(C: float) -> float:
    """
    Converts Celsius to Farenheit
    """
    return C * 1.8 + 32


def _toFeet(m: float) -> float:
    """
    Converts meters to feet
    """
    return m / 0.3048


def _toMeters(ft: float) -> float:
    """
    Converts feet to meters
    """
    return ft * 0.3048


def _organizeDbResults(results: list[tuple], units: int) -> tuple[list[dict], int]:
    """
    Organizes to query output in a list of datapoints.

    Parameters
    ----------
    results: raw results of the DB query
    units: units in which the measurements are returned

    Returns
    ----------
    A list of datapoints, where each datapoint is presented as a dictionary,
    in the following format: {
        'channel_id': str,
        'measurement_id': str,
        'datetime_utc': datetime object,
        'data_id': str,
        'temperature_c'/'temperature_f': float,
        'depth_m'/'depth_ft': float
    }
    Also calculates the approximate size of the output for logging.
    """
    output = list()
    byteSize = 0
    for row in results:
        # Units need to be valid
        assert units in [METRIC, IMPERIAL]
        if units == METRIC:
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datetime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            output.append(datapoint)

        if units == IMPERIAL:
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datetime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_f": _toFarenheit(row[4]),
                "depth_ft": _toFeet(row[5]),
            }
            output.append(datapoint)
        # to estimate the size, we take the string length and use that. If we include overhead, it should be ~ equal
        byteSize += len(str(row))

    return output, byteSize


def getDataOutages() -> list[dict]:
    """
    Finds all data outages or errors in the database.

    Returns
    ------------
    A list of dictionaries, one for each outage that has been
    recorded in the history of the database.
    """

    # Use a helper function to create the query
    query = createEntireDataOutageQuery()
    results = list()

    # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
    with connections["geothermal"].cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            datapoint = {
                "outage_id": row[0],
                "channel_id": row[1],
                "outage_type": row[2],
                "start_time": row[3],
                "end_time": row[4],
            }
            results.append(datapoint)
    return results


def getTempVsTimeResults(
    borehole: str,
    depth: str,
    startTime: datetime,
    endTime: datetime,
    units: int,
) -> tuple[list[dict], dict]:
    """
    Returns a list of all data points across all measurements associated with
    the given channel and depth for a given time range.

    Parameters
    ----------
    channel: borehole number (1 through 5)
    depth: depth of temperature measurement
    startTime: start time of the query
    endTime: end time of the query
    units: units in which the measurements are returned

    Returns
    ----------
    A 2-tuple, consisting of:
    1. a list of datapoints, where each datapoint is presented as a dictionary
       in the form (database_column_label:data_point), and
    2. a dictionary with statistics about the executed query for logging purposes
    """
    # Using boreholes.py, we define a custom Borehole class that stores borehole info
    currentBorehole = boreholes[borehole]
    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    # Use a helper function to create the query
    query = createTempVsTimeQuery()
    results = list()

    if units == IMPERIAL:
        depth = _toMeters(depth)

    # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
    with connections["geothermal"].cursor() as cursor:
        # execute query and record elapsed time
        query_start_time = time.time()
        cursor.execute(query, (channel, depth, lafStart, lafBottom, startTime, endTime))
        query_end_time = time.time()

        # Retrieve and organize the query output
        results, byteSizeEstimate = _organizeDbResults(cursor.fetchall(), units)

    queryStats = {
        "query": query,
        "executionTime": query_end_time - query_start_time,
        "totalRecords": len(results),
        "channel": channel,
        "depth": depth,
        "lafStart": lafStart,
        "lafBottom": lafBottom,
        "startTime": startTime,
        "endTime": endTime,
    }
    return results, queryStats


# def getTempVsDepthResults(
#     borehole: str, timestamp: datetime, units: int
# ) -> tuple[list[dict], dict]:
#     """
#     Returns a list of all data points across all measurements associated with
#     the channel at a time around the given timestamp.

#     Parameters
#     ----------
#     channel: borehole number (1 through 5)
#     timestamp: time of the query
#     units: units in which the measurements are returned

#     Returns
#     ----------
#     A 2-tuple, consisting of:
#     1. a list of datapoints, where each datapoint is presented as a dictionary
#        in the form (database_column_label:data_point), and
#     2. a dictionary with statistics about the executed query for logging purposes
#     """

#     # We can't guarantee there's going to be a measurement at the exact time the user provided,
#     # so we create a 30-minute time range, which has to include exactly one measurement.
#     timestampStart = datetime.strptime(timestamp, f"%Y-%m-%d %H:%M:%S")
#     timestampEnd = (timestampStart + timedelta(minutes=30)).strftime(
#         f"%Y-%m-%d %H:%M:%S"
#     )

#     # Using boreholes.py, we define a custom Borehole class that stores borehole info
#     currentBorehole = boreholes[borehole]
#     channel = currentBorehole.getChannel()
#     lafStart = currentBorehole.getStart()
#     lafBottom = currentBorehole.getBottom()

#     # Use a helper function to create the query
#     query = createTempVsDepthQuery()
#     results = list()

#     with connections["geothermal"].cursor() as cursor:
#         # execute query and record elapsed time
#         query_start_time = time.time()
#         cursor.execute(query, (channel, timestamp, timestampEnd, lafStart, lafBottom))
#         query_end_time = time.time()

#         # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
#         results, byteSizeEstimate = _organizeDbResults(cursor.fetchall(), units)

#     queryStats = {
#         "query": query,
#         "executionTime": query_end_time - query_start_time,
#         "totalRecords": len(results),
#     }
#     return results, queryStats


def getTempProfileResultsByDay(
    borehole: str,
    startTime: datetime,
    endTime: datetime,
    dailyTimestamp: datetime,
    units: int,
) -> tuple[list[dict], dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel and depth for a given time range, returning one measurement for
    each day at a given timestamp.

    Parameters
    ----------
    channel: borehole number (1 through 5)
    depth: depth of temperature measurement
    startTime: start time of the query
    endTime: end time of the query
    dailyTimestamp: timestamp of the measurement, doesn't need to be precise
    units: units in which the measurements are returned

    Returns
    ----------
    A 2-tuple, consisting of:
    1. a list of datapoints, where each datapoint is presented as a dictionary
       in the form (database_column_label:data_point), and
    2. a dictionary with statistics about the executed query for logging purposes
    """
    # Using boreholes.py, we define a custom Borehole class that stores borehole info
    currentBorehole = boreholes[borehole]
    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    # We can't guarantee there's going to be a measurement at the exact time the user provided,
    # so we create a 30-minute time range, which has to include exactly one measurement.
    timestampStart = dailyTimestamp
    timestampEnd = timestampStart + timedelta(minutes=30)

    # Use a helper function to create the query
    query = createTempProfileQueryByDay()
    results = list()

    # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
    with connections["geothermal"].cursor() as cursor:
        # execute query and record elapsed time
        query_start_time = time.time()
        cursor.execute(
            query,
            (
                channel,
                lafStart,
                lafBottom,
                startTime,
                endTime,
                timestampStart.time(),
                timestampEnd.time(),
            ),
        )
        query_end_time = time.time()

        # clean results and crudely estimate the size of the query's result
        # as though it were a csv file (1 char of plaintext ~ 1 byte in csv)
        queryOutput = cursor.fetchall()
        results, byteSizeEstimate = _organizeDbResults(queryOutput, units)

    queryStats = {
        "query": query,
        "executionTime": query_end_time - query_start_time,
        "totalRecords": len(results),
        "channel": channel,
        "lafStart": lafStart,
        "lafBottom": lafBottom,
        "startTime": startTime,
        "endTime": endTime,
    }
    return results, queryStats


def getTempProfileResultsByMeasurement(
    borehole: str, startTime: datetime, endTime: datetime, units: int
) -> tuple[list[dict], dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel and depth for a given time range, returning each measurement.
    Don't use it unless the requested time range is short, othewise the output is extremely big

    Parameters
    ----------
    channel: borehole number (1 through 5)
    startTime: start time of the query
    endTime: end time of the query
    units: units in which the measurements are returned

    Returns
    ----------
    A 2-tuple, consisting of:
    1. a list of datapoints, where each datapoint is presented as a dictionary
       in the form (database_column_label:data_point), and
    2. a dictionary with statistics about the executed query for logging purposes
    """
    # Using boreholes.py, we define a custom Borehole class that stores borehole info
    currentBorehole = boreholes[borehole]
    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    # Use a helper function to create the query
    query = createTempProfileQueryByMeasurement()
    results = list()

    # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
    with connections["geothermal"].cursor() as cursor:
        # execute query and record elapsed time
        query_start_time = time.time()
        cursor.execute(query, (channel, lafStart, lafBottom, startTime, endTime))
        query_end_time = time.time()

        # clean results and crudely estimate the size of the query's result
        # as though it were a csv file (1 char of plaintext ~ 1 byte in csv)
        results, byteSizeEstimate = _organizeDbResults(cursor.fetchall(), units)

    queryStats = {
        "query": query,
        "executionTime": query_end_time - query_start_time,
        "totalRecords": len(results),
        "channel": channel,
        "lafStart": lafStart,
        "lafBottom": lafBottom,
        "startTime": startTime,
        "endTime": endTime,
    }
    return results, queryStats


def getTempProfileResults(
    borehole: str,
    startTime: datetime,
    endTime: datetime,
    dailyTimestamp: datetime,
    groupBy: int,
    units: int,
) -> tuple[list[dict], dict]:
    """
    A stand-in function for getting temperature profile, avoids cluttering other files with different function calls.
    Based on the arguments provided, returns a list of all data points across all measurements associated with
    the channel and depth for a given time range, returning each measurement or one measurement for each day.

    Parameters
    ----------
    borehole: borehole number (1 through 5)
    depth: depth of temperature measurement
    startTime: start time of the query
    endTime: end time of the query
    dailyTimestamp: timestamp of the measurement, doesn't need to be precise

    Returns
    ----------
    A 2-tuple, consisting of:
    1. a list of datapoints, where each datapoint is presented as a dictionary
       in the form (database_column_label:data_point), and
    2. a dictionary with statistics about the executed query for logging purposes
    """
    if groupBy == HOURS:
        return getTempProfileResultsByMeasurement(borehole, startTime, endTime, units)
    else:
        return getTempProfileResultsByDay(
            borehole, startTime, endTime, dailyTimestamp, units
        )


def getRawQueryResults(formData: dict[str, str]) -> tuple[list[dict], dict]:
    """
    Returns a list of all datapoints returned upon execution of the raw
    database query, or raises an execption if the query is unsuccessful.

    Parameters
    ----------
    formData: a dictionary containing the data from the submitted user form

    Returns
    ----------
    A 2-tuple, consisting of:
    1. a list of datapoints, where each datapoint is presented as a dictionary
       in the form (database_column_label:data_point), and
    2. a dictionary with statistics about the executed query for logging purposes
    """
    results = list()
    query = formData["rawQuery"]

    ### LIMIT CHECKING ####
    limit = 500000

    limit_clause = re.search(r"\bLIMIT\s+(\d+)\b", query, re.IGNORECASE)

    if limit_clause:
        if int(limit_clause.group(1)) > limit:
            if ";" in query:
                query = re.sub(
                    r"\bLIMIT\s*\d+\b", f"LIMIT {limit};", query, flags=re.IGNORECASE
                )
            else:
                query = re.sub(
                    r"\bLIMIT\s*\d+\b", f"LIMIT {limit}", query, flags=re.IGNORECASE
                )
    else:
        if ";" in query:
            query = query.replace(";", f" LIMIT {limit};")
        else:
            query = f"{query} LIMIT {limit}"

    try:
        with connections["geothermal"].cursor() as cursor:
            # execute query and record elapsed time
            query_start_time = time.time()
            cursor.execute(query)
            query_end_time = time.time()

            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

        for row in results:
            for key in row:
                if row[key] == None:
                    row[key] = "None"

            if "datetime_utc" in row:
                row["datetime_utc"] = row["datetime_utc"].strftime(f"%Y-%m-%d %H:%M:%S")

            if "start_datetime_utc" in row:
                row["start_datetime_utc"] = row["start_datetime_utc"].strftime(
                    f"%Y-%m-%d %H:%M:%S"
                )

            if "end_datetime_utc" in row:
                row["end_datetime_utc"] = row["end_datetime_utc"].strftime(
                    f"%Y-%m-%d %H:%M:%S"
                )

        queryStats = {
            "query": query,
            "executionTime": query_end_time - query_start_time,
            "totalRecords": len(results),
        }
        return results, queryStats

    except Exception as e:
        raise Exception("Database error: " + str(e))
