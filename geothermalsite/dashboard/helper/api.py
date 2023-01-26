import time
import sys
from django.db import connections
from datetime import datetime, timedelta
from .boreholes import boreholes
from .logging import log_query_as_INFO
from .constants import HOURS, DAYS, WEEKS, MONTHS, YEARS, GROUPS


def _createEntireDataOutageQuery() -> str:
    """
    Creates a query for retrieving all data outages

    Returns
    --------
    Formatted query to be executed by the database cursor
    """
    query = f""" SELECT id, channel_id, outage_type, start_datetime_utc, end_datetime_utc
                 FROM measurement_outage
                 """

    return query


def _createTempVsTimeQuery(
    borehole: str, depth: str, startTime: str, endTime: str
) -> str:
    """
    Creates a query for getting temperature vs time results for fixed depth

    Parameters
    -----------
    channel: ID of the borehole to query
    depth: depth of the measurements held constant
    startTime: start of the time range
    endTime: end of the time range

    Returns
    -----------
    Formatted query to be executed by the database cursor
    """

    currentBorehole = boreholes[borehole]

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    query = f"""SELECT channel_id, measurement_id, datetime_utc, D.id,
            temperature_c, depth_m
            FROM dts_data AS D
            INNER JOIN measurement AS M
            ON M.id = measurement_id
            INNER JOIN channel AS H
            ON channel_id = H.id
            INNER JOIN dts_config AS C
            ON dts_config_id = C.id
            WHERE channel_id IN (SELECT id FROM channel WHERE
                                             channel_name='channel {channel}')
            AND ABS(depth_m-{depth}) < step_increment_m/2
            AND laf_m BETWEEN {lafStart} AND {lafBottom}
            AND datetime_utc BETWEEN '{startTime}' AND '{endTime}'
            ORDER BY datetime_utc;
            """

    return query


def _createTempVsDepthQuery(borehole: str, timestamp: datetime) -> str:
    """
    Creates a query for getting temperature vs depth results for fixed depth

    Parameters
    -----------
    channel: ID of the borehole to query
    timestamp: point in time for the query; if no measurements taken at that
        exact moment, the closest measurements are returned instead

    Returns
    -----------
    Formatted query to be executed by the database cursor
    """
    timestampStart = timestamp
    timestampEnd = timestampStart + timedelta(minutes=30)

    currentBorehole = boreholes[borehole]

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafEnd = currentBorehole.getBottom()

    query = f"""SELECT channel_id, measurement_id, datetime_utc, D.id,
            temperature_c, depth_m
            FROM measurement AS M
            INNER JOIN dts_data AS D
            ON M.id = D.measurement_id
            WHERE channel_id IN (SELECT id FROM channel WHERE
                                             channel_name='channel {channel}')
            AND datetime_utc between '{timestampStart}' AND '{timestampEnd}'
            AND laf_m BETWEEN {lafStart} AND {lafEnd}
            ORDER BY depth_m;
            """

    return query


def _createStratigraphyQuery(
    borehole: str, startTime: str, endTime: str, dailyTimestamp: str
) -> str:
    """
    Creates a query for getting temperature vs time and depth for a given borehole

    Parameters
    -----------
    channel: ID of the borehole to query
    startTime: start of the time range
    endTime: end of the time range

    Returns
    -----------
    Formatted query to be executed by the database cursor
    TODO: retrieve the data each day only at a certain timestamp
    -------------------

    """

    currentBorehole = boreholes[borehole]

    channel = currentBorehole.getChannel()
    lafStart = currentBorehole.getStart()
    lafBottom = currentBorehole.getBottom()

    timestampStart = dailyTimestamp
    timestampEnd = timestampStart + timedelta(minutes=30)

    query = f"""SELECT channel_id, measurement_id, datetime_utc, D.id,
            temperature_c, depth_m
            FROM dts_data AS D
            INNER JOIN measurement AS M
            ON M.id = measurement_id
            INNER JOIN channel AS H
            ON channel_id = H.id
            INNER JOIN dts_config AS C
            ON dts_config_id = C.id
            WHERE channel_id IN (SELECT id FROM channel WHERE
                                             channel_name='channel {channel}')
            AND laf_m BETWEEN {lafStart} AND {lafBottom}
            AND datetime_utc BETWEEN '{startTime}' AND '{endTime}'
            AND CAST(datetime_utc AS TIME) BETWEEN '{timestampStart}' AND '{timestampEnd}
            ORDER BY depthm_m;
            """

    return query


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

    query = _createTempVsDepthQuery(borehole, timestamp)
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

    query = _createTempVsTimeQuery(borehole, depth, startTime, endTime)
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


def getStratigraphyResults(
    borehole: str, startTime: str, endTime: str, dailyTimestamp: str
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
    query = _createStratigraphyQuery(borehole, startTime, endTime, dailyTimestamp)
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

    query = _createEntireDataOutageQuery()
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
