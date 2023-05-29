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


def createTempVsTimeQuery() -> str:
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
                                             channel_name='channel %s')
            AND ABS(depth_m-%s) < step_increment_m/2
            AND laf_m BETWEEN %s AND %s
            AND datetime_utc BETWEEN %s AND %s
            ORDER BY datetime_utc;
            """

    return query


# def createTempVsDepthQuery() -> str:
#     """
#     Creates a query for getting temperature vs depth results for fixed depth

#     Parameters
#     -----------
#     channel: ID of the borehole to query
#     timestamp: point in time for the query; if no measurements taken at that
#         exact moment, the closest measurements are returned instead

#     Returns
#     -----------
#     Formatted query to be executed by the database cursor
#     """

#     query = f"""SELECT channel_id, measurement_id, datetime_utc, D.id,
#             temperature_c, depth_m
#             FROM measurement AS M
#             INNER JOIN dts_data AS D
#             ON M.id = D.measurement_id
#             WHERE channel_id IN (SELECT id FROM channel WHERE
#                                              channel_name='channel %s')
#             AND datetime_utc between %s AND %s
#             AND laf_m BETWEEN %s AND %s
#             ORDER BY depth_m;
#             """

#     return query


def createTempProfileQueryByDay() -> str:
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

    # old query
    # query = f"""SELECT channel_id, measurement_id, datetime_utc, D.id,
    #         temperature_c, depth_m
    #         FROM dts_data AS D
    #         INNER JOIN measurement AS M
    #         ON M.id = measurement_id
    #         INNER JOIN channel AS H
    #         ON channel_id = H.id
    #         INNER JOIN dts_config AS C
    #         ON dts_config_id = C.id
    #         WHERE channel_id IN (SELECT id FROM channel WHERE
    #                                          channel_name='channel %s')
    #         AND laf_m BETWEEN %s AND %s
    #         AND datetime_utc BETWEEN %s AND %s
    #         AND CAST(datetime_utc AS TIME) BETWEEN %s AND %s
    #         ORDER BY depth_m, datetime_utc;
    #         """

    # new, streamlined query
    # This new query is identical to the query formed by createTempProfileQueryByMeasurement()
    # because of this it may be possible to streamline further and declutter the code by removing one of these functions
    query = f"""SELECT M.channel_id, D.measurement_id, M.datetime_utc, D.id, 
            D.temperature_c, D.depth_m 
            FROM dts_data AS D 
            INNER JOIN measurement AS M 
            ON M.id = D.measurement_id 
            INNER JOIN channel AS H 
            ON M.channel_id = H.id 
            INNER JOIN dts_config AS C 
            ON H.dts_config_id = C.id 
            WHERE C.id IN (SELECT id FROM dts_config WHERE 
                                        configuration_name = '2019-02-26-geothermal_config' 
                                        OR configuration_name = 'geothermal-config-2019-05-15') 
            AND M.channel_id IN (SELECT id FROM channel WHERE 
                                        channel_name = 'channel %s') 
            AND laf_m BETWEEN %s AND %s 
            AND datetime_utc BETWEEN %s AND %s 
            ORDER BY depth_m, datetime_utc;
            """

    return query


def createTempProfileQueryByMeasurement() -> str:
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
                                             channel_name='channel %s')
            AND laf_m BETWEEN %s AND %s
            AND datetime_utc BETWEEN %s AND %s
            ORDER BY depth_m, datetime_utc;
            """

    return query
