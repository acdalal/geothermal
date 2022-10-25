import sys
import psycopg2
import config
import json

def getConnection() -> psycopg2.connection:

    '''
    Returns a database connection object with which you can create cursors,
    issue SQL queries, etc.

    Parameters
    -----------
    None

    Returns
    ------------
    A psycopg2 cursor object
    '''

    try:
        return psycopg2.connect(database=config.DATABASE,
                                user=config.USER,
                                password=config.PASSWORD)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()


def executeDBQuery(connection: psycopg2.connection, query: str) -> list[tuple]:
    '''
    Executes the passed query on the database and throws an exception if it encounters an error.

    Parameters
    -------------
    connection: A psycongp2 connection object for the database

    query: The query to be excuted


    Returns
    ------------
    The output of the query

    '''

    try:
        cursor = connection.cursor()
        # Execute the query
        cursor.execute(query)
        queryResult = cursor.fetchall()
        cursor.close()
        return queryResult
    except Exception as e:
        print(e, file=sys.stderr)


def findOutagesInUserData(startTime: str, endTime: str) -> list[tuple]:
    '''
    Finds all data outages or errors in the given time range.

    Parameters
    ------------
    startTime: a timestamp for the start of the time range in UTC time format.
    endTIme: a timestamp for the end of the time range in UTC time format. To get info on outages for only one timestamp, pass the same value for startTime and endTime.

    Returns
    ------------
    A list of tuples (outageID, startTime, endTime, outageType) for each outage that happenned during the requested time range.
    If no outages happenned, returns an empty list.

    '''

    query = f''' SELECT outage_type_id, start_datetime_utc, end_datetime_utc, outage_type
                 FROM measurement_outage, outage_types
                 WHERE (start_datetime_utc BETWEEN {startTime} AND {endTime}) OR (end_datetime_utc BETWEEN {startTime} AND {endTime}) OR ({startTime} >= start_datetime_utc AND {endTime} <= end_datetime_utc'''
    try:
        connection = getConnection()
        allOutages = executeDBQuery(connection, query)
        return allOutages
    except Exception as e:
        print(e, file=sys.stderr)

def createTempVsTimeQuery(channel: int, depth: str) -> dict:

    '''
    Returns the results of the query for temp vs time

    Parameters

    -----------
    channel
    depth

    Returns

    -----------
    JSON formatted temperature vs time data for constant depth


    '''

    query = '''SELECT channel_id, measurement_id, datetime_utc, dts_data.id,
                    dts_data.temperature_c, dts_data.datetime_utc
                FROM measurement, dts_data
                WHERE measurement.channel_id IN (SELECT id FROM channel
                                                WHERE channel_name = 'chanel %s')
                AND measurement.depth_m
                AND measurement.id = dts_data.measurement_id'''

    results = []


    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(query, (channel, depth))

        for row in cursor:
            datapoint = {'channel_id':row[0],
                        'measurement_id':row[1],
                        'datetime_utc':row[2].strftime(f"%Y-%,-%d %H:%M:%S"),
                        'data_id':row[3],
                        'temperature_c':row[4],
                        'datetime': row[5]}

            results.append(datapoint)
    except Exception as e:
        print(e, file = sys.stderr)

    return json.dumps(results)
