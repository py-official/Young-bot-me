# python lib
import os

# project lib
from .yaml_manager import load_yaml_file

# dirs
CDIR = os.getcwd() + "/"
DIR_DATA = CDIR + "data/"
DIR_CONFS = DIR_DATA + "conf/"
DIR_CONF_YAML = DIR_CONFS + "yaml/"
DIR_CONF_YAML_DYNAMIC = DIR_CONF_YAML + "dynamic/"
DIR_CONF_YAML_STATIC = DIR_CONF_YAML + "static/"
DIR_LOGS = DIR_DATA + "logs/"

# file names
FILE_NAME_CONF_DYNAMIC_OLD_MOUSE = "dynamic_old_mouse_config"
FILE_NAME_CONF_DYNAMIC_YOUNG_MOUSE = "dynamic_young_mouse_config"
FILE_NAME_CONF_STATIC = "static_config"
FILE_NAME_CONF_STATIC_PROJECT = "static_project_config"
FILE_NAME_CONF_LOG = "dynamic_log_config"

# file types
FILE_TYPE_YAML_CONFS = ".yaml"
FILE_TYPE_LOGS = ".log"
FILE_TYPE_LOGS_ARCHIVE = ".zip"

"""
'dynamic_old_mouse_config.yaml' - dynamic config for the old mouse;
'dynamic_young_mouse_config.yaml' - dynamic config for the young mouse;
'static_config.yaml' - static config for other people to fill out the config;
'static_project_config.yaml' - static config used in the project itself;
"""

# create path to static configs
_file_path_to_static_config = DIR_CONF_YAML_STATIC + FILE_NAME_CONF_STATIC + FILE_TYPE_YAML_CONFS
_file_path_to_static_project_config = DIR_CONF_YAML_STATIC + FILE_NAME_CONF_STATIC_PROJECT + FILE_TYPE_YAML_CONFS

# loading static configs
_static_config_data = load_yaml_file(_file_path_to_static_config)
_static_project_config_data = load_yaml_file(_file_path_to_static_project_config)

# logs
LOG_LINE_NUM_MAX = _static_project_config_data["log_line_num_max"]
LOG_FILE_NUM_MAX_IN_ARCHIVE = _static_project_config_data["log_file_num_max_in_archive"]
LOG_TIME_DEL_ARCHIVE = _static_project_config_data["log_time_del_archive"]
LOG_DATE_FORMAT = _static_project_config_data["log_date_format"]
