from flask.ext import restful, sqlalchemy
from flask import Flask

from finder.util import fileutil

app = Flask(__name__)

# Set root folder for loading files
fileutil.set_root(__file__)
fileutil.load_config(app.config, '.config')

api = restful.Api(app)
db = sqlalchemy.SQLAlchemy(app)
