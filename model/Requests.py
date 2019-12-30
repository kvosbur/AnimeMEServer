from app import db

TABLE_NAME = "requests"


class Requests(db.Model):
    __tablename__ = TABLE_NAME
    requestID = db.Column(db.Integer, primary_key=True)
    englishName = db.Column(db.String(255), nullable=True)
    jpName = db.Column(db.String(255), nullable=True)
    type = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    requestUserID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    animeID = db.Column(db.Integer, db.ForeignKey('anime.animeID'), nullable=True)

