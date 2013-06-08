from flask.ext import restful, sqlalchemy
from flask import Flask

from finder.util import set_root, load_config

app = Flask(__name__)

# Set root folder for loading files
set_root(__file__)
load_config(app.config, '.config')

api = restful.Api(app)
db = sqlalchemy.SQLAlchemy(app)

import finder.views
