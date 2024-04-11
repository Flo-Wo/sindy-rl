import os
import logging
import yaml
from pprint import pprint


def read_dyna_config(_parent_dir: str, filename: str, verbose: bool = True):
    """Read the config.yml file given the parent_dir and the filename, print all."""
    filename = os.path.join(_parent_dir, "config_templates", filename)

    # load config
    with open(filename, "r") as f:
        dyna_config = yaml.load(f, Loader=yaml.SafeLoader)
    if verbose:
        pprint(dyna_config)
    return dyna_config


def setup_folders(global_config: dict):
    """
    Create the main folder (if not existing) and the logging subfolder.
    Save the config file into the main folder.
    """
    # setup the main folder
    folder_path = _get_folder_path(global_config)
    _create_dir_if_not_exists(folder_path)

    # save the config file to reconstruct the experiment in the future
    with open(folder_path + "/exp_config.yml", "w") as yaml_file:
        yaml.dump(global_config, yaml_file, default_flow_style=False)

    # setup the logger subfolder
    logger_path = get_logger_folder(global_config)
    _create_dir_if_not_exists(logger_path)


def _get_folder_path(global_config: dict):
    global_dir = global_config.get("global_dir")
    folder_name = global_config.get("folder_name")
    return global_dir + folder_name


def get_logger_folder(global_config: dict):
    """Combine the global dir, with exp. dir and the logger folder."""
    logdir = global_config.get("log_dir", None)
    if logdir is None:
        return None
    folder_path = _get_folder_path(global_config)
    return folder_path + logdir


def _create_dir_if_not_exists(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        logging.info("Path {} already existed.".format(path))
