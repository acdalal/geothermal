import time
from django.db import connections
from datetime import datetime, timedelta
from .boreholes import boreholes



def _createDataOutageQuery(startTime: str, endTime: str) -> str:
    """
    Creates a query for retrieving data outages during the selected period of time

    Paramete
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


def _createTempVsDepthQuery(borehole: str, timestamp: str) -> str:

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
    startTime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    endTime = startTime + timedelta(minutes=30)

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
            AND datetime_utc between '{startTime}' AND '{endTime}'
            AND laf_m BETWEEN {lafStart} AND {lafEnd}
            ORDER BY depth_m;
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


def getTempVsDepthResults(borehole: str, timestamp: str) -> list[dict]:
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

    query = _createTempVsDepthQuery(borehole, timestamp)
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
    borehole: str, depth: str, startTime: str, endTime: str
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

    query = _createTempVsTimeQuery(borehole, depth, startTime, endTime)
    print("got the query")
    results = list()
    startTime = time.time()
    with connections["geothermal"].cursor() as cursor:
        print("sending query")
        
        cursor.execute(query)
        print("finished executing query")
        print("RUNTIME:", (time.time() - startTime))
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
