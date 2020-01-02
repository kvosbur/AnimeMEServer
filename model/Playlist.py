from model import db

TABLE_NAME = "playlist"


class Playlist(db.Model):
    __tablename__ = TABLE_NAME
    playlistID = db.Column(db.Integer, primary_key=True)
    playlistName = db.Column(db.String(255), nullable=False)
    createdDate = db.Column(db.DateTime(), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    songs = db.relationship("PlaylistSong", backref="playlist", cascade="all, delete-orphan")
