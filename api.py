import sys
import psycopg2
import config


def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.DATABASE,
                                user=config.USER,
                                password=config.PASSWORD)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()


''' Execute DB queries with psycopg2 and return the queried results directly
    before closing the connection'''


def executeDBQuery(connection, query):
    try:
        cursor = connection.cursor()
        # Execute the query
        cursor.execute(query)
        queryResult = cursor.fetchall()
        cursor.close()
        return queryResult
    except Exception as e:
        print(e, file=sys.stderr)


def findOutagesInUserData(startTime, endTime):
    query = f''' SELECT outage_type_id, start_datetime_utc, end_datetime_utc, outage_type 
                 FROM measurement_outage, outage_types 
                 WHERE (start_datetime_utc BETWEEN {startTime} AND {endTime}) OR (end_datetime_utc BETWEEN {startTime} AND {endTime}) OR ({startTime} >= start_datetime_utc AND {endTime} <= end_datetime_utc'''
    try:
        connection = get_connection()
        allOutages = executeDBQuery(connection, query)
        return allOutages
    except Exception as e:
        print(e, file=sys.stderr)
