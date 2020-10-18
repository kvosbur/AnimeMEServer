from model import db
from model.Anime import Anime

class AnimeHandler:

    @staticmethod
    def addAnime(animeNameEn, animeNameJP, releaseDate, animeImageUrl):
        animeObj = Anime(animeNameEN=animeNameEn,
              animeNameJP=animeNameJP,
              releasedDate=releaseDate,
              imageURL=animeImageUrl)

        db.session.add(animeObj)
        db.session.commit()
        return animeObj.animeID
