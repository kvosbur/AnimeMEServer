
from dotenv import load_dotenv
import os
from flask import Flask
from flask_migrate import Migrate
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from util import FileHandler

load_dotenv('.env')
app = Flask(__name__)
app.config['FLASK_ENV'] = os.environ['FLASK_ENV']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['SERVER_NAME'] = os.environ['SERVER_NAME']
FileHandler.folderPath = os.environ['folderPath']
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from model import Anime
from model import Friends
from model import Playlist
from model import PlaylistSong
from model import Requests
from model import Song
from model import User


if __name__ == "__main__":
    app.run()
