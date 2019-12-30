from app import db

TABLE_NAME = "song"


class Song(db.Model):
    __tablename__ = TABLE_NAME
    songID = db.Column(db.Integer, primary_key=True)
    songNameEN = db.Column(db.String(200), nullable=False)
    songNameJP = db.Column(db.String(200), nullable=False)
    songType = db.Column(db.Integer, nullable=False)
    songTypeValue = db.Column(db.Integer, nullable=True)
    animeID = db.Column(db.Integer, db.ForeignKey('anime.animeID'))
