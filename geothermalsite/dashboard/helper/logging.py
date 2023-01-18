import sys

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


def log_info_for_query(query: str, execution_time: int, bytes: int):
    """Logs information about the executed query as an INFO type

    Parameters
    ----------
    query : str
        the PostgreSQL query that was executed
    execution_time : int
        the time it took to execute the query
    bytes : int
        the sum of the byte sizes of every entry in cursor.fetchall()

    Returns
    -------
    Nothing; writes the log on a single line to the logfile specified in
    settings.py
    """

    # ip_address = get_user_ip_address(request)
    oneline_query = convert_multiline_to_oneline(query)

    logger.info(
        "{} | {}s | {}bytes".format(
            oneline_query,
            execution_time,
            bytes,
        )
    )
