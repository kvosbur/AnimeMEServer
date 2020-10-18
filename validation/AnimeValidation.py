import validators
from datetime import datetime
from model import db
from model.Anime import Anime
from sqlalchemy import or_


class AnimeValidation:

    @staticmethod
    def validateAnimeUniqueness(animeNameEn, animeNameJp):
        """Validates whether this is the first time the email is being used or not"""
        isFound = db.session.query(Anime).filter(
            or_(Anime.animeNameJP == animeNameJp, Anime.animeNameEN == animeNameEn)).first()
        if isFound is not None:
            return 1
        return None

    @staticmethod
    def validateAnimeCreate(animeNameEn, animeNameJP, releaseDate, animeImageUrl):
        """Validates whether the the anime creation details were passed correctly"""
        if animeNameEn == "" and animeNameJP == "":
            return "Name must be given in at least one language"
        elif AnimeValidation.validateAnimeUniqueness(animeNameEn, animeNameJP):
            return "Anime already exists"
        elif not validators.url(animeImageUrl):
            return "Url for image must be in valid format"

        try:
            datetime.strptime('%m/%d/%Y', releaseDate)
            return None
        except ValueError:
            return "Date must be correctly formatted as mm/dd/yyyy"
