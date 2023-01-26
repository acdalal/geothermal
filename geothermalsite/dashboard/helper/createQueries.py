from .boreholes import boreholes
from datetime import timedelta, datetime


def createEntireDataOutageQuery() -> str:
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


def createTempVsTimeQuery(
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


def createTempVsDepthQuery(borehole: str, timestamp: datetime) -> str:
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


def createStratigraphyQueryByDay(
    borehole: str, startTime: str, endTime: str, dailyTimestamp: str
) -> str:
    """
    Creates a query for getting temperature vs time and depth for a given borehole, returning one measurement for each day

    Parameters
    -----------
    channel: ID of the borehole to query
    startTime: start of the time range
    endTime: end of the time range

    Returns
    -----------
    Formatted query to be executed by the database cursor

    TODO
    -------------------
    Replace the hardcoded 30 minutes increment to the timestamp with a dynamically updated increment

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
            AND CAST(datetime_utc AS TIME) BETWEEN '{timestampStart}' AND '{timestampEnd}'
            ORDER BY depth_m, datetime_utc;
            """

    return query


def createStratigraphyQueryByMeasurement(
    borehole: str,
    startTime: str,
    endTime: str,
) -> str:
    """
    Creates a query for getting temperature vs time and depth for a given borehole, returning each measurement

    Parameters
    -----------
    channel: ID of the borehole to query
    startTime: start of the time range
    endTime: end of the time range

    Returns
    -----------
    Formatted query to be executed by the database cursor
    -------------------

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
            AND laf_m BETWEEN {lafStart} AND {lafBottom}
            AND datetime_utc BETWEEN '{startTime}' AND '{endTime}'
            ORDER BY depth_m, datetime_utc;
            """

    return query