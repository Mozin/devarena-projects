from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json

from src.common.jwt_helper import create_token_obj_bundle
from src.common.utils import Utils
from src.models.users.user import User

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/login", methods=["POST"])
@expects_json(
    {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', "password"]
    }
)
def user_login():
    '''User Login
    ---
   tags:
   - Users
   consumes:
   - "application/json"
   parameters:
   - in: "body"
     name: "body"
     required: true
     schema:
       type: "object"
       properties:
         email:
           type: "string"
         password:
           type: "string"
   responses:
    200:
      description: User object with token
    400:
      description: Invalid input | MISSING_INPUT_KEYS | USER_NOT_FOUND | INCORRECT_PASSWORD
   '''
    email = request.json["email"]
    password = request.json["password"]

    if not Utils.check_required_keys_present(request.json, ["email", "password"]):
        return jsonify({"response": "MISSING_INPUT_KEYS"}), 400

    existing_user = User.find_user_by_email(email)
    if not existing_user:
        return jsonify({"response": "USER_NOT_FOUND"}), 400

    if not Utils.check_hashed_password(password, existing_user.password):
        return jsonify({"response" : "INCORRECT_PASSWORD"}), 403

    return jsonify(create_token_obj_bundle(existing_user)), 200
