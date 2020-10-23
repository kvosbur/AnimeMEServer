from model import db

TABLE_NAME = "anime"


class Anime(db.Model):
    __tablename__ = TABLE_NAME
    animeID = db.Column(db.Integer, primary_key=True)
    animeNameEN = db.Column(db.String(200), nullable=False)
    animeNameJP = db.Column(db.String(200), nullable=False)
    releasedDate = db.Column(db.Date(), nullable=False)
    imageURL = db.Column(db.String(255), nullable=True)

    seasons = db.relationship("Season", backref="anime", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.animeID,
            "nameEnglish": self.animeNameEN,
            "nameJapanese": self.animeNameJP,
            "songCount": sum([len(season.songs) for season in self.seasons]),
            "image": self.imageURL
        }
