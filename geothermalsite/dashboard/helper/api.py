import time
import sys
from django.db import connections
from datetime import datetime
from .logging import log_query_as_INFO
from .createQueries import (
    createEntireDataOutageQuery,
    createStratigraphyQueryByMeasurement,
    createStratigraphyQueryByDay,
    createTempVsDepthQuery,
    createTempVsTimeQuery,
)
from .constants import DAYS, HOURS


def getTempVsDepthResults(borehole: str, timestamp: datetime) -> list[dict]:
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

    query = createTempVsDepthQuery(borehole, timestamp)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query)
        query_end_time = time.time()

        # clean results and record query result size
        total_bytes = 0
        for row in cursor.fetchall():
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datetime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            results.append(datapoint)
            total_bytes += sys.getsizeof(row)

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            total_bytes,
        )

    return results


def getTempVsTimeResults(
    borehole: str, depth: str, startTime: datetime, endTime: datetime
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

    query = createTempVsTimeQuery(borehole, depth, startTime, endTime)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query)
        query_end_time = time.time()

        # clean results and record query result size
        total_bytes = 0
        for row in cursor.fetchall():
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datetime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            results.append(datapoint)
            total_bytes += sys.getsizeof(row)

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            total_bytes,
        )
    return results


def getStratigraphyResultsByDay(
    borehole: int, startTime: datetime, endTime: datetime, dailyTimestamp: datetime
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
    query = createStratigraphyQueryByDay(borehole, startTime, endTime, dailyTimestamp)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query)
        query_end_time = time.time()

        # clean results and record query result size
        totalBytes = 0
        for row in cursor.fetchall():
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datetime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            results.append(datapoint)
            totalBytes += sys.getsizeof(datapoint)

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            totalBytes,
        )
    return results


def getStratigraphyResultsByMeasurement(
    borehole: str, startTime: str, endTime: str
) -> list[dict]:
    """
    Returns a list of all data points across all measurements associated with
    the channel and depth for a given time range, returning each measurement. Don't use it unless the requested time range is short, othewise the output is extremely big

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
    query = createStratigraphyQueryByMeasurement(borehole, startTime, endTime)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query)
        query_end_time = time.time()

        # clean results and record query result size
        totalBytes = 0
        for row in cursor.fetchall():
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datetime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            results.append(datapoint)
            totalBytes += sys.getsizeof(datapoint)

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            totalBytes,
        )

    return results


def getDataOutages() -> list[dict]:
    """
    Finds all data outages or errors in the database.

    # TODO: re-write this documentation, since this function takes no
    #       parameters, but the below information may still be useful elsewhere

    Parameters
    ------------
    startTime: a timestamp for the start of the time range in UTC time format.
    endTime: a timestamp for the end of the time range in UTC time format.
        To get info on outages for only one timestamp, pass the same value
        for startTime and endTime.

    Returns
    ------------
    A list of tuples (outageID, channelID, outageType, start_datetime_utc,
    end_datetime_utc) for each outage that happened during the requested
    time range. If no outages happened, returns an empty list.
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


def getStratigraphyResults(
    borehole: str, startTime: str, endTime: str, dailyTimestamp: str, groupBy: int
) -> list[dict]:
    if groupBy == HOURS:
        return getStratigraphyResultsByMeasurement(borehole, startTime, endTime)
    else:
        return getStratigraphyResultsByDay(borehole, startTime, endTime, dailyTimestamp)
