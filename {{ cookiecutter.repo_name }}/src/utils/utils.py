import yaml
import argparse
from dotenv import find_dotenv, load_dotenv


def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def get_config():
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    return read_params(parsed_args.config)


def dotenv_loader():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
