from model import db

TABLE_NAME = "friends"


class PlaylistSong(db.Model):
    __tablename__ = TABLE_NAME
    source = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False, primary_key=True)
    recipient = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
