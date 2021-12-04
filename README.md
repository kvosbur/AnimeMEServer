# AnimeMEServer
This is the server side application for the AnimeMeClient repository.

For better ways to do the automated documentation with swagger use the below website with an in depth
explanation https://flask-restplus.readthedocs.io/en/stable/swagger.html

To run locally for testing it is best to use "flask run --host=0.0.0.0" so 
you can access it on local network.

process for migration is:
flask db init
flask db migrate -m "message"
flask db upgrade



https://dassum.medium.com/python-rest-apis-with-flask-connexion-and-sqlalchemy-3c8c3292d9ce