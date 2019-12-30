from app import db

TABLE_NAME = "user"


class User(db.Model):
    __tablename__ = TABLE_NAME
    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    sessionToken = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    playlists = db.relationship("Playlist", backref="user", cascade="all, delete-orphan")
