from .base import BaseTestCase, db
from model.User import User
from model.Anime import Anime
from model.Song import Song
from model.AnimeSeason import Season
import datetime
from parameterized import parameterized

USEAUTHCODE = "ROAMGdIz6K8zRiWYMQFZyxfMd4u96dqobs5eiAF1DuYTnANEfNJnu5vuvGGzN2aCeIe4sUdTPpqsBlEQYmuTUr7RV4nFk81po4QPEry4YeQVQtOnqy58zzFbnmub7s5B"


class AnimeBaseTestCase(BaseTestCase):
    def setUp(self):
        db.create_all()

        userObj = User(email="a@a.com",
                       username="AwesomeSauce",
                       sessionToken="69f6f1e7eddcb33b790474e010e7476ee15a7950527b50271f9892fcc7100a99ec752826363893be2c7e43b4b5935e1965d09178bacf10e1fbbd317a6aa86b6d",
                       password="w01sdXe24fhb13Vs9QVfARBfjy8mvTvPj6z9iExgJWYA7tvBzdz9tUKQCGC8yrAT$df23b65963ae7852854aef5c729a8eb3ef9b5dd24f87abaf517a3882a2dbff763ca8a9a5b132d8984356587dd23f0e914a7f5eee652cba0fe5aba5b175333f8c",
                       adminType=0)
        db.session.add(userObj)

        self.animeObj = Anime(animeNameEN="",
              animeNameJP="japanese",
              releasedDate=datetime.datetime.now(),
              imageURL="google.com")

        self.animeObj1 = Anime(animeNameEN="english",
                         animeNameJP="",
                         releasedDate=datetime.datetime.now(),
                         imageURL="google.com1")
        db.session.add(self.animeObj)
        db.session.add(self.animeObj1)

        seasonObj = Season(seasonNumber=1)

        self.animeObj1.seasons = [seasonObj]


        songObj1 = Song(songNameEN="english",
                       songNameJP="japanese",
                       songArtist="artist",
                       songType=0,
                       songTypeValue=6)

        songObj2 = Song(songNameEN="english1",
                        songNameJP="japanese1",
                        songArtist="artist1",
                        songType=0,
                        songTypeValue=6)

        seasonObj.songs = [songObj1, songObj2]

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestAnimeDetailPost(AnimeBaseTestCase):

    def test_empty_auth_code(self):
        payload = {"animeNameEN": "awesomeName",
                   "animeNameJP": "anotherName",
                   "releaseDate": "01/01/2005",
                   "animeImage": "google.com"}
        headers = {}

        with self.client:
            response = self.client.post(
                "anime/detail",
                headers=headers,
                data=payload
            )

            assert response.status_code == 400
            assert response.json == {
                'errors': {'authCode': 'Missing required parameter in the HTTP headers'},
                'message': 'Input payload validation failed'}

    def test_empty_anime_names(self):
        payload = {"animeNameEN": "",
                   "animeNameJP": "",
                   "releaseDate": "01/01/2005",
                   "animeImage": "google.com"}
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.post(
                "anime/detail",
                headers=headers,
                data=payload
            )

            assert response.status_code == 400
            assert response.json == {'message': 'Name must be given in at least one language'}

    def test_anime_name_en_duplicate(self):
        payload = {"animeNameEN": "english",
                   "animeNameJP": "otherJapanese",
                   "releaseDate": "01/01/2005",
                   "animeImage": "google.com"}
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.post(
                "anime/detail",
                headers=headers,
                data=payload
            )

            assert response.status_code == 400
            assert response.json == {'message': 'Anime already exists'}

    def test_anime_name_jp_duplicate(self):
        payload = {"animeNameEN": "otherEnglish",
                   "animeNameJP": "japanese",
                   "releaseDate": "01/01/2005",
                   "animeImage": "google.com"}
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.post(
                "anime/detail",
                headers=headers,
                data=payload
            )

            assert response.status_code == 400
            assert response.json == {'message': 'Anime already exists'}

    def test_anime_url_invalid(self):
        payload = {"animeNameEN": "otherEnglish",
                   "animeNameJP": "otherJapanese",
                   "releaseDate": "01/01/2005",
                   "animeImage": "invalid"}
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.post(
                "anime/detail",
                headers=headers,
                data=payload
            )

            assert response.status_code == 400
            assert response.json == {'message': 'Url for image must be in valid format'}

    def test_anime_valid(self):
        englishName = 'otherEnglish'
        japaneseName = ''
        releasedDate = '01/01/2005'
        imageUrl = 'https://google.com'
        payload = {"animeNameEN": englishName,
                   "animeNameJP": japaneseName,
                   "releaseDate": releasedDate,
                   "animeImage": imageUrl}
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.post(
                "anime/detail",
                headers=headers,
                data=payload
            )

            assert response.status_code == 200
            assert response.json == {'message': 'OK'}

            animeObj = db.session.query(Anime).filter_by(animeNameEN=englishName).first()
            assert animeObj is not None
            assert animeObj.animeNameJP == japaneseName
            assert animeObj.releasedDate == datetime.date(year=2005, month=1, day=1)
            assert animeObj.imageURL == imageUrl
            assert len(animeObj.seasons) == 1
            assert animeObj.seasons[0].seasonNumber == 1
            assert animeObj.seasons[0].imageURL == imageUrl


class TestAnimeFeedGet(AnimeBaseTestCase):

    def test_no_name_given(self):
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.get(
                "anime/feed",
                headers=headers,
            )

            assert response.status_code == 200
            assert response.json == {"data": [self.animeObj.to_json(), self.animeObj1.to_json()]}

    def test_english_name_given(self):
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.get(
                "anime/feed?animeNameEN=english",
                headers=headers,
            )

            assert response.status_code == 200
            assert response.json == {"data": [self.animeObj1.to_json()]}

    def test_japanese_name_given(self):
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.get(
                "anime/feed?animeNameJP=nes",
                headers=headers,
            )

            assert response.status_code == 200
            assert response.json == {"data": [self.animeObj.to_json()]}


class TestAnimeDetaildGet(AnimeBaseTestCase):

    def test_no_id_given(self):
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.get(
                "anime/detail",
                headers=headers,
            )

            assert response.status_code == 400
            assert response.json == {'errors': {'animeId': 'Missing required parameter in the query string'},
                                     'message': 'Input payload validation failed'}

    def test_id_has_no_match(self):
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.get(
                "anime/detail?animeId=-1",
                headers=headers,
            )

            assert response.status_code == 200
            assert response.json == {'data': {}}

    def test_valid_id(self):
        headers = {"authCode": USEAUTHCODE}

        with self.client:
            response = self.client.get(
                "anime/detail?animeId=" + str(self.animeObj1.animeID),
                headers=headers,
            )

            assert response.status_code == 200
            assert response.json['data']['id'] == self.animeObj1.animeID
            assert len(response.json['data']['seasons']) == len(self.animeObj1.seasons)
            assert len(response.json['data']['seasons'][0]['songs']) == len(self.animeObj1.seasons[0].songs)




