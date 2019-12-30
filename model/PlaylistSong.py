from app import db

TABLE_NAME = "playlistsong"


class PlaylistSong(db.Model):
    __tablename__ = TABLE_NAME
    playlistID = db.Column(db.Integer, db.ForeignKey('playlist.playlistID'), primary_key=True)
    songID = db.Column(db.Integer, db.ForeignKey('song.songID'), primary_key=True)
    position = db.Column(db.Integer, nullable=False)
