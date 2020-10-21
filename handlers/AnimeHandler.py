from model import db
from model.Anime import Anime
import datetime


class AnimeHandler:

    @staticmethod
    def addAnime(animeNameEn, animeNameJP, releaseDate, animeImageUrl):
        dateObj = datetime.datetime.strptime(releaseDate, '%m/%d/%Y').date()

        animeObj = Anime(animeNameEN=animeNameEn,
              animeNameJP=animeNameJP,
              releasedDate=dateObj,
              imageURL=animeImageUrl)

        db.session.add(animeObj)
        db.session.commit()
        return animeObj.animeID

    @staticmethod
    def feedAnime(animeNameEn, animeNameJp):
        models = db.session.query(Anime).filter(Anime.animeNameEN.like("%" + animeNameEn + "%"),
                                                Anime.animeNameJP.like("%" + animeNameJp + "%")).all()

        return [model.to_json() for model in models]
