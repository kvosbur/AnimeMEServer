
from flask_restx import Resource, reqparse, Namespace, fields
from validation.AnimeValidation import AnimeValidation
from handlers.AnimeHandler import AnimeHandler
from util.HTTPResponse import HTTPResponse
from .Auth import auth_required

anime = Namespace('anime', description='Anime Information')


animeCreationResponse = anime.model("AnimeCreationResponse", {"message": fields.String(example="OK")})

animeResponseModel = anime.model("AnimeCreationResponse", {"data": fields.String(example="Anime details")})


@anime.route("/detail")
class AnimeDetail(Resource):
    createParser = reqparse.RequestParser()
    createParser.add_argument('animeNameEN', type=str, location='form', required=True)
    createParser.add_argument('animeNameJP', type=str, location='form', required=True)
    createParser.add_argument('releaseDate', type=str, location='form', required=True)
    createParser.add_argument('animeImage', type=str, location='form', required=True)

    @anime.expect(createParser)
    @anime.response(200, "Anime was created successfully", animeCreationResponse)
    @anime.response(400, "Input Validation", animeCreationResponse)
    @auth_required
    def post(self, userObj):
        arguments = self.createParser.parse_args()
        nameEn = arguments["animeNameEN"]
        nameJp = arguments["animeNameJP"]
        releaseDate = arguments["releaseDate"]
        imageUrl = arguments["animeImage"]
        errMsg = AnimeValidation.validateAnimeCreate(nameEn, nameJp, releaseDate, imageUrl)
        # Input did not pass input validation
        if errMsg is not None:
            return HTTPResponse.makeResponseMinimal(400, errMsg)

        # create a new anime
        AnimeHandler.addAnime(nameEn, nameJp, releaseDate, imageUrl)

        return HTTPResponse.makeResponseMinimal(200, "OK")

    getParser = reqparse.RequestParser()
    getParser.add_argument('animeId', type=int, location='args', required=True)

    @anime.expect(getParser)
    @anime.response(200, "Anime was retrieved successfully", animeResponseModel)
    @anime.response(400, "Input Validation", animeCreationResponse)
    @auth_required
    def get(self, userObj):
        arguments = self.getParser.parse_args()
        animeId = arguments.get("animeId") or ""

        details = AnimeHandler.detailAnime(animeId)
        formattedDetails = {}
        if details is not None:
            formattedDetails = details.to_detailed_json()
        return {"data": formattedDetails}, 200


@anime.route("/feed")
class AnimeFeed(Resource):
    createParser = reqparse.RequestParser()
    createParser.add_argument('animeNameEN', type=str, location='args', required=False)
    createParser.add_argument('animeNameJP', type=str, location='args', required=False)

    @anime.expect(createParser)
    @anime.response(200, "Anime was created successfully", animeCreationResponse)
    @anime.response(400, "Input Validation", animeCreationResponse)
    @auth_required
    def get(self, userObj):
        arguments = self.createParser.parse_args()
        nameEn = arguments.get("animeNameEN") or ""
        nameJp = arguments.get("animeNameJP") or ""

        return {"data": AnimeHandler.feedAnime(nameEn, nameJp)}, 200
