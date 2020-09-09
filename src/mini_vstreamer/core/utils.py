import logging
import yaml

def read_yml_file(path):
    with open(path, 'rb') as config_file:
        try:
            return yaml.load(config_file)
        except yaml.YAMLError as exc:
            logging.info(exc)
            raise ValueError(exc)
