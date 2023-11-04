from flask import Flask, make_response, jsonify
from flasgger import Swagger
from jsonschema.exceptions import ValidationError

import src
from src.common.database import Database


def create_app():
    app = Flask(__name__)
    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"] = f'postgresql://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f'postgresql://postgres:rvsabc1234@rvsdb.c1jshtxodiud.ap-south-1.rds.amazonaws.com:5432/rvsdb'
    app.secret_key = 'super secret key'
    Database.initialize(app)

    return app


app = create_app()

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
src.jwt.init_app(app)

from src.models.users.users_controller import users_blueprint
from src.models.projects.projects_controller import projects_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(projects_blueprint, url_prefix="/projects")

swagger_template = {
        "swagger" : "2.0",
        "info": {
            "title" : "Devarena Project Development"
        },
        "securityDefinitions": {
            "bearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
}


swag = Swagger(app, template=swagger_template)



@app.route("/")
def hello_world():
    """
    End point for testing
    """
    return "API works"


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'response': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error

app.run(debug = True, host="0.0.0.0")
