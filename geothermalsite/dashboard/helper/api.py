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
    return C * 9 / 5 + 32


def _toFeet(m: float) -> float:
    return m / 0.3048


def _organizeDbResults(results: list[tuple], units: int) -> tuple[list[dict], int]:
    output = list()
    byteSize = 0
    for row in results:
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
    the channel and depth for a given time range.

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

    currentBorehole = boreholes[borehole]

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    query = createTempVsTimeQuery()
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query, (channel, depth, lafStart, lafBottom, startTime, endTime))
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


def getTempVsDepthResults(borehole: str, timestamp: datetime, units: int) -> list[dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel during that hour.

    Parameters
    ----------
    channel: ID of the borehole (1 or 3)
    timestamp: start time of the query

    Returns
    ----------
    A dictionary with the query data (column label:data point)
    """

    timestampStart = datetime.strptime(timestamp, f"%Y-%m-%d %H:%M:%S")
    timestampEnd = (timestampStart + timedelta(minutes=30)).strftime(
        f"%Y-%m-%d %H:%M:%S"
    )

    currentBorehole = boreholes[borehole]

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafEnd = currentBorehole.getBottom()

    query = createTempVsDepthQuery()
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query, (channel, timestamp, timestampEnd, lafStart, lafEnd))
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


def getTempProfileResultsByDay(
    borehole: str, startTime: str, endTime: str, dailyTimestamp: str, units: int
) -> list[dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel and depth for a given time range, returning one measurement for each day at a given timestamp

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
    query = createTempProfileQueryByDay()
    results = list()

    currentBorehole = boreholes[borehole]

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    timestampStart = dailyTimestamp
    timestampEnd = timestampStart + timedelta(minutes=30)

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
    print(results)
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
    query = createTempProfileQueryByMeasurement(borehole, startTime, endTime)
    results = list()

    currentBorehole = boreholes[borehole]

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

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

    query = createEntireDataOutageQuery()
    results = list()

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

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        try:
            cursor.execute(query)
            query_end_time = time.time()

            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            # log the query execution as an INFO log
            log_query_as_INFO(
                query,
                # query_end_time - query_start_time,
                len(results),
            )

        except:
            results = SyntaxError

    return results
