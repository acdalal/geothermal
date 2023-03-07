import time
import sys
from .boreholes import boreholes
from django.db import connections
from datetime import timedelta, datetime
from .logging import log_query_as_INFO
from .createQueries import (
    createEntireDataOutageQuery,
    createTempProfileQueryByDay,
    createTempProfileQueryByMeasurement,
    createTempVsDepthQuery,
    createTempVsTimeQuery,
)
from .constants import HOURS, METRIC, IMPERIAL


def _toFarenheit(C: float) -> float:
    """
    Converts Celsius to Farenheit
    """
    return C * 9 / 5 + 32


def _toFeet(m: float) -> float:
    """
    Converts meters to feet
    """
    return m / 0.3048


def _organizeDbResults(results: list[tuple], units: int) -> tuple[list[dict], int]:
    """
    Organizes to query output in a list of datapoints. Each datapoint is presented as a dictionary,
    in the following format: {'channel_id': str, 'measurement_id': str, 'datetime_utc': datetime object, 'data_id': str, 'temperature_c'/'temperature_f': float, 'depth_m'/'depth_ft': float}
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


def getTempVsTimeResults(
    borehole: str,
    depth: str,
    startTime: datetime,
    endTime: datetime,
    units: int,
) -> list[dict]:
    """
    Returns a list of all data points across all measurements associated with
    the given channel and depth for a given time range.

    Parameters
    ----------
    channel: ID of the borehole (1 or 3)
    depth: depth of temperature measurement
    startTime: start time of the query
    endTime: end time of the query

    Returns
    ----------
    A dictionary with the results of the query
    """
    # Using boreholes.py, we define a custom Borehole class that stores borehole info
    currentBorehole = boreholes[borehole]
    # Easily retrieve borehole info
    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    # Use a helper function to create the query
    query = createTempVsTimeQuery()
    results = list()

    # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query, (channel, depth, lafStart, lafBottom, startTime, endTime))
        query_end_time = time.time()

        # Retrieve and organize the query output
        results, byteSizeEstimate = _organizeDbResults(cursor.fetchall(), units)

        # Log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            byteSizeEstimate,
        )

    return results


def getTempVsDepthResults(borehole: str, timestamp: datetime, units: int) -> list[dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel at a time around the given timestamp.

    Parameters
    ----------
    channel: ID of the borehole (1 or 3)
    timestamp: time of the query

    Returns
    ----------
    A dictionary with the query data (column label:data point)
    """

    # We can't guarantee there's going to be a measurement at the exact time the user provided,
    # so we create a 30-minute time range, which has to include exactly one measurement.
    timestampStart = datetime.strptime(timestamp, f"%Y-%m-%d %H:%M:%S")
    timestampEnd = (timestampStart + timedelta(minutes=30)).strftime(
        f"%Y-%m-%d %H:%M:%S"
    )

    # Using boreholes.py, we define a custom Borehole class that stores borehole info
    currentBorehole = boreholes[borehole]
    # Easily retrieve borehole info
    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    # Use a helper function to create the query
    query = createTempVsDepthQuery()
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query, (channel, timestamp, timestampEnd, lafStart, lafBottom))
        query_end_time = time.time()

        # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
        results, byteSizeEstimate = _organizeDbResults(cursor.fetchall(), units)

        # Log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            byteSizeEstimate,
        )

    return results


def getTempProfileResultsByDay(
    borehole: str, startTime: str, endTime: str, dailyTimestamp: str, units: int
) -> list[dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel and depth for a given time range, returning one measurement for
    each day at a given timestamp.

    Parameters
    ----------
    channel: ID of the borehole (1 or 3)
    depth: depth of temperature measurement
    startTime: start time of the query
    endTime: end time of the query
    dailyTimestamp: timestamp of the measurement, doesn't need to be precise

    Returns
    ----------
    A dictionary with the results of the query
    """
    # Using boreholes.py, we define a custom Borehole class that stores borehole info
    currentBorehole = boreholes[borehole]
    # Easily retrieve borehole info
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
        # record query execution time
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

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            len(results),
        )
    return results


def getTempProfileResultsByMeasurement(
    borehole: str, startTime: str, endTime: str, units: int
) -> list[dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel and depth for a given time range, returning each measurement.
    Don't use it unless the requested time range is short, othewise the output is extremely big

    Parameters
    ----------
    channel: ID of the borehole (1 or 3)
    depth: depth of temperature measurement
    startTime: start time of the query
    endTime: end time of the query

    Returns
    ----------
    A dictionary with the results of the query
    """
    # Using boreholes.py, we define a custom Borehole class that stores borehole info
    currentBorehole = boreholes[borehole]
    # Easily retrieve borehole info
    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    # Use a helper function to create the query
    query = createTempProfileQueryByMeasurement()
    results = list()

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    # geothermalsite/settings.py has the DB credentials, which let us access the database cursor like this.
    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query, (channel, lafStart, lafBottom, startTime, endTime))
        query_end_time = time.time()

        # clean results and crudely estimate the size of the query's result
        # as though it were a csv file (1 char of plaintext ~ 1 byte in csv)
        results, byteSizeEstimate = _organizeDbResults(cursor.fetchall(), units)

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            len(results),
        )

    return results


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


def getTempProfileResults(
    borehole: str,
    startTime: str,
    endTime: str,
    dailyTimestamp: str,
    groupBy: int,
    units: int,
) -> list[dict]:
    """ """
    if groupBy == HOURS:
        return getTempProfileResultsByMeasurement(borehole, startTime, endTime, units)
    else:
        return getTempProfileResultsByDay(
            borehole, startTime, endTime, dailyTimestamp, units
        )


def getRawQueryResults(formData: dict[str, str]) -> list[dict]:
    results = list()
    query = formData["rawQuery"]

    ### SANITIZE QUERY HERE ####

    try:
        with connections["geothermal"].cursor() as cursor:
            # record query execution time
            query_start_time = time.time()
            cursor.execute(query)
            query_end_time = time.time()

            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            # log the query execution as an INFO log
            log_query_as_INFO(
                query,
                query_end_time - query_start_time,
                len(results),
            )
        for row in results:
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

        return results
    except Exception as e:
        raise Exception("Database error: " + str(e))
