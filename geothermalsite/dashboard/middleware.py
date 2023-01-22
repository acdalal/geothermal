"""This file contains middleware that is executed as specified in
geothermalsite/settings.py. In essence, middleware is code that is
executed to process a request/response and can do work before/after
the corresponding view is called, adding extra functionality to the
request/response processing.

See Django documentation for more:
https://docs.djangoproject.com/en/4.1/topics/http/middleware/
"""

import logging
from django.utils.deprecation import MiddlewareMixin


class IPLogMiddleware(MiddlewareMixin):
    """Middleware class for logging user IP addresses when certain views are run"""

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Logs the IP addr of the user that triggered a DB query view function

        If the view function triggers a database query, this method logs the IP
        address of the user along with the query they are executing. The views that
        trigger a database query are hard-coded into this method as a temporary
        solution.
        """

        db_query_views = [
            "tempVsTime",
            "tempVsTimeDownload",
            "tempVsDepth",
            "tempVsDepthDownload",
        ]

        if view_func.__name__ in db_query_views:
            ip_address = request.META.get("REMOTE_ADDR")
            logging.info(
                f"IP Address: {ip_address} executing {view_func.__name__} query"
            )
