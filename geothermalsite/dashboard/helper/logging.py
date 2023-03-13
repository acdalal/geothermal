# configure logger for DB queries
import logging

logger = logging.getLogger(__name__)


def convert_multiline_to_oneline(s: str) -> str:
    """Converts the given string to a oneline string"""

    return "\t".join([line.strip() for line in s.splitlines()])


def get_user_ip_address(request):
    """Gets the IP address of the user who submitted the POST request

    Warning
    -------
    request.META.get('REMOTE_ADDR') is easily spoofed by malicious users,
    and should not be used for security purposes.
    """

    ip_address = request.META.get("REMOTE_ADDR")
    return ip_address


def log_query_as_INFO(
    userIP: str, query: str, execution_time: int, number_of_records_returned: int
):
    """Logs information about the executed query at INFO level

    Parameters
    ----------
    userIP: str
        the IP address of the user that executed the query
        (see warning in get_user_ip_address)
    query : str
        the PostgreSQL query that was executed
    execution_time : int
        the time it took to execute the query in seconds
    number_of_records_returned : int
        the number of records returned from the database

    Returns
    -------
    Nothing; writes the log on a single line to the logfile specified in settings.py
    """
    oneline_query = convert_multiline_to_oneline(query)
    logger.info(
        "User IP: {} | query: {} | query execution time: {}s | number of records returned: {}".format(
            userIP,
            oneline_query,
            execution_time,
            number_of_records_returned,
        )
    )
