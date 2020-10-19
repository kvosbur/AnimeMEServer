
from dotenv import load_dotenv
import os
import click
import sys
import pytest
from flask import Flask
from flask_migrate import Migrate
from util import FileHandler
from routes import api
from model import db

load_dotenv('.env')
app = Flask(__name__)
app.config['FLASK_ENV'] = os.environ['FLASK_ENV']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['SERVER_NAME'] = os.environ['SERVER_NAME']
FileHandler.folderPath = os.environ['folderPath']
api.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

DEBUG = True

from model import Anime
from model import Friends
from model import Playlist
from model import PlaylistSong
from model import Requests
from model import Song
from model import User


@app.cli.command('test')
@click.argument('testname', required=False)
def test(testname):
    if testname is None:
        returnVal = pytest.main(
            ['-W', 'ignore::DeprecationWarning', '--cov', '--cov-config=./.coveragec', '--rootdir', './tests'])
        sys.exit(returnVal)
    else:
        returnVal = pytest.main(['-W', 'ignore::DeprecationWarning', './tests/test_{}.py'.format(testname)])
        sys.exit(returnVal)


if __name__ == "__main__":
    app.run()
