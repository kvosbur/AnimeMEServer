from model import db

TABLE_NAME = "song"


class Song(db.Model):
    __tablename__ = TABLE_NAME
    songID = db.Column(db.Integer, primary_key=True)
    songNameEN = db.Column(db.String(200), nullable=False)
    songNameJP = db.Column(db.String(200), nullable=False)
    songArtist = db.Column(db.String(200), nullable=False)
    songType = db.Column(db.Integer, nullable=False)
    songTypeValue = db.Column(db.Integer, nullable=True)
    seasonId = db.Column(db.Integer, db.ForeignKey('season.seasonId'))

    def to_json(self):
        return {
            "songId": self.songID,
            "songNameEn": self.songNameEN,
            "songNameJp": self.songNameJP,
            "songArtist": self.songArtist,
            "songType": self.songType,
            "songTypeValue": self.songTypeValue
        }
