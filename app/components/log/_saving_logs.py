# python lib
import datetime
import os
from zipfile import ZipFile
from pathlib import Path
from logging import ERROR, CRITICAL, INFO, DEBUG, WARNING, NOTSET
from typing import Callable
from functools import wraps
import time
from glob import glob

# project lib
from ..config import (
    DIR_LOGS,
    FILE_NAME_CONF_LOG,
    FILE_TYPE_YAML_CONFS,
    FILE_TYPE_LOGS,
    LOG_LINE_NUM_MAX,
    LOG_FILE_NUM_MAX_IN_ARCHIVE,
    FILE_TYPE_LOGS_ARCHIVE,
    LOG_TIME_DEL_ARCHIVE,
    LOG_DATE_FORMAT,
)
from ..yaml_manager import load_yaml_file, dump_yaml_file

_DESCRIPTION_LEVELS = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}

_DESCRIPTION_NAME_LEVELS = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}


# decorator for adding execution of the write_log_to_file function.
def decorator_write_log_to_file(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        # saving original message
        message = args[1]

        # modification of the “args” tuple
        args = list(args)
        args[1] = func.__name__.upper() + f":{args[0].name}:" + args[1]
        args = tuple(args)

        result = func(*args, **kwargs)

        # writing logs using data from 'func'
        write_log_to_file(message, args[0].name, _DESCRIPTION_NAME_LEVELS[func.__name__.upper()])

        return result

    return wrapper


def _del_archives(today_date: str) -> None:  # function for deleting archives with logs after a certain amount of time
    # convert date to seconds
    today_date_sec = _convert_date_to_sec(LOG_DATE_FORMAT, today_date)

    # getting paths to archives with logs
    archives_to_dir_logs = glob(DIR_LOGS + "*" + FILE_TYPE_LOGS_ARCHIVE)

    for path_to_archive in archives_to_dir_logs:
        # getting the archive name and removing unnecessary elements from the received name
        name_archive = Path(path_to_archive)
        name_archive = name_archive.name.split(name_archive.suffix)[0].split("_")[0]

        """
        Calculates the difference between the current date and the archive creation date, 
        and then compares it with a given number.
        If the condition is true, then the archive with logs will be deleted.
        """
        if today_date_sec - _convert_date_to_sec(LOG_DATE_FORMAT, name_archive) >= LOG_TIME_DEL_ARCHIVE:
            os.remove(path_to_archive)


# function to convert date to seconds from the beginning of the epoch
def _convert_date_to_sec(date_format: str, date: str) -> float:
    # создания объекта даты
    date_obj = datetime.datetime.strptime(date, date_format)

    # converting date object to seconds
    time_stamp = time.mktime(date_obj.timetuple())

    return time_stamp


def write_log_to_file(message: object, name: str, level: int) -> None:  # function for writing logs to a file
    # creating var for a path to file 'dynamic_log_config.yaml'
    path_data_logs = DIR_LOGS + FILE_NAME_CONF_LOG + FILE_TYPE_YAML_CONFS

    # opening a file 'data_log.yaml' and loading data for creating logs.
    data_log: dict = load_yaml_file(path_data_logs)

    """
    checks whether this level is in the _DESCRIPTION_LEVELS dictionary, 
    if it is not found, replaces the level value with NOTSET.
    """
    if level not in _DESCRIPTION_LEVELS.keys():
        level = NOTSET

    # getting the current date and generating a message to write to the log file.
    today_date = str(datetime.datetime.now().date())
    message = f"[{datetime.datetime.now().time()}] {name}: {_DESCRIPTION_LEVELS[level]}: {message}\n"

    # checking the date of archives and if they exist for more than a specified time, they will be deleted
    _del_archives(today_date)

    # will replace with the current date if 'now_date' or 'old_date' is None.
    if data_log["now_date"] is None:
        data_log["now_date"] = today_date

    if data_log["old_date"] is None:
        data_log["old_date"] = today_date

    # creating a log file path using the Path class and creating an archive file path using the Path class.
    path_now_log = Path(DIR_LOGS + data_log["now_date"] + "_" + str(data_log["num_log"]) + FILE_TYPE_LOGS)
    path_now_logs_archive = Path(DIR_LOGS + data_log["now_date"] + "_" + str(data_log["num_archive"]) +
                                 FILE_TYPE_LOGS_ARCHIVE)

    # checks if the date has changed
    data_log["now_date"] = today_date
    if data_log["now_date"] != data_log["old_date"]:
        data_log["old_date"] = today_date
        data_log["num_log"] = 0
        data_log["log_line_num"] = 1

    # creating/adding a message to the log file
    with open(str(path_now_log), "a+") as log_file:
        log_file.write(message)

        data_log["log_line_num"] += 1

    """
    checks how many lines were written to the log file, 
    if the lines in the log file are greater than or equal to LOG_LINE_NUM_MAX, 
    then the log file will be archived.
    """
    if data_log["log_line_num"] >= LOG_LINE_NUM_MAX:
        # creating an archive with logs if it does not exist
        if not os.path.exists(str(path_now_logs_archive)):
            with ZipFile(str(path_now_logs_archive), "w") as file_logs_archive:
                file_logs_archive.close()

        # opening the archive and writing a log file
        with ZipFile(str(path_now_logs_archive), "a") as file_logs_archive:
            file_logs_archive.write(filename=str(path_now_log), arcname=path_now_log.name)

            # getting a list of files from the archive
            files_in_archive = file_logs_archive.namelist()

        # deleting the log file added to the archive and changing/resetting indexes.
        os.remove(str(path_now_log))
        data_log["num_log"] += 1
        data_log["log_line_num"] = 1

        """
        checks how many files are in the archive; 
        if the number of files is greater than or equal to LOG_FILE_NUM_MAX_IN_ARCHIVE, 
        then it updates the num_archive index.
        """
        if len(files_in_archive) >= LOG_FILE_NUM_MAX_IN_ARCHIVE:
            data_log["num_archive"] += 1

    # writing data to dynamic_log_config.yaml
    dump_yaml_file(path_data_logs, data_log)
