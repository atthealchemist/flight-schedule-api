from datetime import datetime
from pathlib import Path

import yaml
import json
import base64


def fetch_airports_from_json():
    with open('assets/airports.json', 'r+') as file:
        content = file.read()
        return json.loads(content)


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def calculate_flight_duration(start, end):
    start_time = datetime.fromisoformat(start).time()
    end_time = datetime.fromisoformat(end).time()

    now = datetime.now()
    start_time = datetime.combine(now, start_time)
    end_time = datetime.combine(now, end_time)

    duration = end_time - start_time
    return str(duration)[:-3]


def parse_time_from_date_string(date_string):
    return str(datetime.fromisoformat(date_string).time())[:-3]


def load_config(section=False, config_path='config.yml'):
    config_path = Path(config_path)
    config = config_path
    # we can't find config in program folder
    if not config_path.exists():
        print("Config file {} was not found!".format(config_path))
        config = False
    with open(config, 'r+') as yaml_config:
        yaml_contents = yaml_config.read()
        config = yaml.safe_load(yaml_contents)
    if section:
        config = config.get(section)
    return config
