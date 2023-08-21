from sqlmodel import Field, SQLModel, create_engine

import os
import yaml
from pathlib import Path

_current_dir = os.path.dirname(os.path.abspath(__file__))
#print(current_dir)

def read_yaml(file):
    with open(file, "r") as f:
        data = yaml.safe_load(f)
    return data

def load_config():

    #read application config
    appfile = Path(_current_dir).parent.parent.joinpath("resource/application.yaml")
    _conf = read_yaml(appfile)
    print(_conf)

    return _conf

_conf = load_config()

BACKEND_ADDRESS= _conf["server"]["address"] + ":" + str(_conf["server"]["port"])
DB_URL = _conf["database"]["url"]

SECRET_KEY = _conf["auth"]["secret_key"]
ALGORITHM = _conf["auth"]["algorithm"]

db_engine = create_engine(DB_URL)

