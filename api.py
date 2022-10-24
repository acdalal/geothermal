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


def executeDBQuery(connection, query):
    try:
        cursor = connection.cursor()
        # Execute the query
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e, file=sys.stderr)
