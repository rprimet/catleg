from catala_devtools_fr.config import settings


def set_basic_loglevel():
    """
    Utility for setting the log level as per config -- meant to be used
    within CLI tools only.

    To use, set CATDEV_LOG_LEVEL=INFO in the environment
    or LOG_LEVEL in the .catdev.toml configuration file
    """
    log_level = settings.get("log_level").upper()
    if log_level is not None:
        import logging

        logging.basicConfig(level=log_level)