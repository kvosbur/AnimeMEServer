from model import db

TABLE_NAME = "season"


class Season(db.Model):
    __tablename__ = TABLE_NAME
    seasonId = db.Column(db.Integer, primary_key=True)
    seasonNumber = db.Column(db.Integer, nullable=True)
    seasonName = db.Column(db.String(200), nullable=True)
    imageURL = db.Column(db.String(255), nullable=True)
    animeID = db.Column(db.Integer, db.ForeignKey('anime.animeID'))
    songs = db.relationship("Song", backref="season", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "seasonId": self.seasonId,
            "seasonNumber": self.seasonNumber,
            "seasonName": self.seasonName,
            "image": self.imageURL,
        }
