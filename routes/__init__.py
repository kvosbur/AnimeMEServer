from flask_restx import Api

from .User import user
from .Anime import anime

api = Api(
    title='AnimeMe Documentation',
    version='1.0',
    description='This is the API documentation for the AnimeME mobile application server.',
)

api.add_namespace(user)
api.add_namespace(anime)
