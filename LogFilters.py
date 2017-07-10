"""Logging filters for local use."""
import logging
import platform


class HostnameFilter(logging.Filter):
    """Filter to insert a hostname record."""

    def filter(self, record):
        """Filter function."""
        hostname = platform.node().split('.')[0]
        record.hostname = hostname
        return 1
