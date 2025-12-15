import logging
import sys


def setup_project_root_logging(level: int | None = None) -> logging.Logger:
    logger_name = "bike_geometry_comparator"
    logger = logging.getLogger(logger_name)

    # Set level (default INFO)
    effective_level = level if level is not None else logging.INFO
    logger.setLevel(effective_level)

    # Create stdout handler if absent
    def _is_stdout_handler(h: logging.Handler) -> bool:
        return (
            isinstance(h, logging.StreamHandler)
            and getattr(h, "stream", None) is sys.stdout
        )

    if not any(_is_stdout_handler(h) for h in logger.handlers):
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(effective_level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Avoid double logging via root logger
    logger.propagate = False

    return logger
