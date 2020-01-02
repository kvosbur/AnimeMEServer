from flask_restplus import Api

from .User import user

api = Api(
    title='AnimeMe Documentation',
    version='1.0',
    description='This is the API documentation for the AnimeME mobile application server.',
)

api.add_namespace(user)
