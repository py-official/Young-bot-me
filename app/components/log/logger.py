# python lib
import logging
import functools
from typing import Callable, Type
import sys

# my lib
from _saving_logs import decorator_write_log_to_file


class CustomLogger(logging.Logger):
    def __init__(self, name: str, level: int):
        super().__init__(name, level)

    @decorator_write_log_to_file
    def debug(
            self,
            msg,
            *args,
            exc_info=None,
            stack_info=False,
            stacklevel=1,
            extra=None,
    ):
        super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @decorator_write_log_to_file
    def info(
            self,
            msg,
            *args,
            exc_info=None,
            stack_info=False,
            stacklevel=1,
            extra=None,
    ):
        super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @decorator_write_log_to_file
    def warning(
            self,
            msg,
            *args,
            exc_info=None,
            stack_info=False,
            stacklevel=1,
            extra=None,
    ):
        super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @decorator_write_log_to_file
    def error(
            self,
            msg,
            *args,
            exc_info=None,
            stack_info=False,
            stacklevel=1,
            extra=None,
    ):
        super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @decorator_write_log_to_file
    def critical(
            self,
            msg,
            *args,
            exc_info=None,
            stack_info=False,
            stacklevel=1,
            extra=None,
    ):
        super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)


def _send_error(
        custom_logger: logging.Logger,
        error: Type[Exception],
        text_log: str,
        program_exit: bool
) -> None:
    if text_log is not None:
        custom_logger.error(text_log)

    else:
        custom_logger.error(f"{type(error)}: {error}\n{error.__doc__}")

    if program_exit:
        custom_logger.info("API has stopped working!")
        sys.exit(1)


def error_catcher(
        custom_logger: logging.Logger,
        error_type: Type[Exception],
        text_log: str | None = None,
        program_exit: bool = False,
        work: bool = True,
):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if work:
                try:
                    result = func(*args, **kwargs)

                    return result

                except error_type as e:
                    # checking logging level
                    if custom_logger.level == logging.ERROR:
                        _send_error(custom_logger, e, text_log, program_exit)

                    else:
                        # output warning if logging level is too low
                        logger = CustomLogger(name=custom_logger.name, level=logging.WARN)
                        logger.warning(
                            msg=f"Your \"CustomLogger\" has too low a "
                                f"logging(CustomLogger.level < logging.ERROR) level. At this logging level, "
                                f"no message will be displayed. "
                                f"Please set the logging level to 40 or higher. "
                                f"Error message encountered in your function:\n{type(e)}: {e}\n{e.__doc__}"
                        )

            else:
                result = func(*args, **kwargs)

                return result

        return wrapper

    return decorator
