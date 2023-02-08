import time
import sys
from .boreholes import boreholes
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

        # clean results and crudely estimate the size of the query's result
        # as though it were a csv file (1 char of plaintext ~ 1 byte in csv)
        csv_byte_size_estimate = 0
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

            csv_byte_size_estimate += len(str(row))

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            csv_byte_size_estimate,
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
        csv_byte_size_estimate = 0
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

            csv_byte_size_estimate += len(str(row))

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            csv_byte_size_estimate,
        )
    return results


def getStratigraphyResultsByDay(
    borehole: str, startTime: str, endTime: str, dailyTimestamp: str
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

        # clean results and crudely estimate the size of the query's result
        # as though it were a csv file (1 char of plaintext ~ 1 byte in csv)
        csv_byte_size_estimate = 0
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

            csv_byte_size_estimate += len(str(row))

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            csv_byte_size_estimate,
        )

    return results


def getStratigraphyResultsByMeasurement(
    borehole: str, startTime: str, endTime: str
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
    query = createStratigraphyQueryByMeasurement(borehole, startTime, endTime)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        # record query execution time
        query_start_time = time.time()
        cursor.execute(query)
        query_end_time = time.time()

        # clean results and crudely estimate the size of the query's result
        # as though it were a csv file (1 char of plaintext ~ 1 byte in csv)
        csv_byte_size_estimate = 0
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

            csv_byte_size_estimate += len(str(row))

        # log the query execution as an INFO log
        log_query_as_INFO(
            query,
            query_end_time - query_start_time,
            csv_byte_size_estimate,
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
