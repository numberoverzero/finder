from flask import Flask

from finder.util import set_root, load_file_config, load_env_config

env_vars = [
    'SQLALCHEMY_DATABASE_URI'
]

app = Flask(__name__)

# Set root folder for loading files
set_root(__file__)
load_file_config(app.config, '.config')
load_env_config(app.config, env_vars, overwrite_null=False)

import finder.models
db = finder.models.db

import finder.views
