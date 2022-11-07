import sys
from django.http import HttpResponse
from django.db import connections
from datetime import datetime, timedelta
import psycopg2
from . import config
import json
from datetime import datetime, timedelta
import dateparser as dp


def _createDataOutageQuery(startTime: str, endTime: str) -> str:
    """
    Creates a query for retrieving data outages during the selected period of time

    Parameters
    -----------
    startTime: start of the time range
    endTime: end of the time range

    Returns
    -----------
    Formatted query to be executed by the database cursor

    """

    query = f""" SELECT outage_type_id, start_datetime_utc, end_datetime_utc, outage_type
                 FROM measurement_outage, outage_types
                 WHERE (start_datetime_utc BETWEEN {startTime} AND {endTime}) OR
                 (end_datetime_utc BETWEEN {startTime} AND {endTime}) OR
                 ({startTime} >= start_datetime_utc AND {endTime} <= end_datetime_utc)"""

    return query


def _createTempVsTimeQuery(
    channel: int, depth: str, startTime: str, endTime: str
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

    query = f"""SELECT channel_id, measurement_id, datetime_utc, dts_data.id,
            dts_data.temperature_c, dts_data.depth_m
            FROM measurement
            JOIN dts_data
            ON measurement.id = dts_data.measurement_id
            WHERE measurement.channel_id IN (SELECT id FROM channel WHERE
                                             channel_name={channel})
            AND dt_data.depth_m = {depth}
            limit 5;
            """

    return query


def _createTempVsDepthQuery(channel: int, timestamp: str) -> str:

    """
    Creates a query for getting temperature vs depth results for fixed depth

    Parameters
    -----------
    channel: ID of the borehole to query
    timestamp: point in time for the query; if no measurements taken at that exact moment, the closest measurements are returned instead

    Returns
    -----------
    Formatted query to be executed by the database cursor


    """
    startTime = datetime.strptime(timestamp, "%Y/%m/%d %H:%M")
    endTime = startTime + timedelta(hours=1)

    query = f"""SELECT channel_id, measurement_id, datetime_utc, dts_data.id,
            dts_data.temperature_c, dts_data.depth_m
            FROM measurement
            JOIN dts_data
            ON measurement.id = dts_data.measurement_id
            WHERE measurement.channel_id IN (SELECT id FROM channel WHERE
                                             channel_name='channel {channel}')
            AND measurement.datetime_utc between {startTime} AND {endTime}
            """

    return query


def _countMeasurement(request) -> list[tuple]:
    """
    Proof of concept query
    """
    query = "select COUNT(*) from measurement"
    with connections["geothermal"].cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results


def getTempVsDepthResults(channel: int, timestamp: str) -> list[dict]:
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

    Example
    ----------
    TODO
    """

    query = _createTempVsDepthQuery(channel, timestamp)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        cursor.execute(query)

        for row in cursor.fetchall():
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datatime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            results.append(datapoint)

    return results


def getTempVsTimeResults(
    channel: int, depth: str, startTime: str, endTime: str
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

    Example
    ----------
    TODO
    """
    query = _createTempVsTimeQuery(channel, depth, startTime, endTime)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datatime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            results.append(datapoint)

    return results


def getDataOutages(startTime: str, endTime: str) -> list[tuple]:
    """
    Finds all data outages or errors in the given time range.

    Parameters
    ------------
    startTime: a timestamp for the start of the time range in UTC time format.
    endTIme: a timestamp for the end of the time range in UTC time format. To get info on outages for only one timestamp, pass the same value for startTime and endTime.

    Returns
    ------------
    A list of tuples (outageID, startTime, endTime, outageType) for each outage that happenned during the requested time range.
    If no outages happenned, returns an empty list.

    """

    query = _createDataOutageQuery(startTime, endTime)
    results = list()

    with connections["geothermal"].cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            datapoint = {
                "outage_id": row[0],
                "start_time": row[1],
                "end_time": row[2],
                "outage_type": row[3],
            }
            results.append(datapoint)
    return results
