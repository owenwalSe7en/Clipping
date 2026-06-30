import logging
import logging.handlers
from pathlib import Path


def setup_logging(app):
    log_dir = Path(app.root_path) / "logs"
    log_dir.mkdir(exist_ok=True)

    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "prescreener.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.DEBUG)

    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=2 * 1024 * 1024,
        backupCount=3,
    )
    error_handler.setFormatter(fmt)
    error_handler.setLevel(logging.ERROR)

    root = logging.getLogger("prescreener")
    root.setLevel(logging.DEBUG)
    root.addHandler(file_handler)
    root.addHandler(error_handler)

    if app.debug:
        stream = logging.StreamHandler()
        stream.setFormatter(fmt)
        stream.setLevel(logging.DEBUG)
        root.addHandler(stream)

    app.logger.handlers = root.handlers
    app.logger.setLevel(root.level)

    return root
