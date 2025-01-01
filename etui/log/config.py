import logging
import coloredlogs


def setup_logging(datefmt: str = "%H:%M:%S", level: int = logging.INFO) -> logging.Logger:
    """Set up logging for the application. This function should be called at the beginning of the application, ideally in the in your __init__.py file.

    Args:
        datefmt (_type_, optional): _description_. Defaults to "%H:%m:%S".
        level (logging.Level, optional): _description_. Defaults to logging.INFO.

    Returns:
        logging.Logger: _description_
    """
    logger = logging.getLogger()
    coloredlogs.install(
        datefmt=datefmt,
        level=level,
        fmt="%(asctime)s | %(levelname)s | %(message)s",
    )

    return logger


def set_subprocess_log_level(logger_name: str, logger_level: int):
    """Change log level for a specific logger

    Args:
        logger_name (str): Name of logger, for example: "json"
        logger_level (logging.Level): Level of logging, for example: logging.DEBUG
    """
    try:
        logging.getLogger(logger_name).setLevel(level=logger_level)
    except Exception as e:
        logging.error(f"Failed to set log level for {logger_name} - {logger_level}: {e}")
