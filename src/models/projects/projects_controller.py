from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json

from src.common.jwt_helper import create_token_obj_bundle, get_user_identity
from src.common.utils import Utils
from src.models.projects.project import Project
from src.models.users.user import User

projects_blueprint = Blueprint("projects", __name__)


@projects_blueprint.route("/create", methods=["POST"])
@expects_json(
    {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'description': {'type': 'string'},
        'completed' : {'type' : 'boolean'}
    },
    'required': ['title', "description", 'completed']
    }
)
def create_project():
    '''Create Project
    ---
   tags:
   - Projects
   security: [ { 'bearerAuth': [] } ]
   consumes:
   - "application/json"
   parameters:
   - in: "body"
     name: "body"
     required: true
     schema:
       type: "object"
       properties:
         title:
           type: "string"
         description:
           type: "string"
         completed:
           type: "boolean"
   responses:
    200:
      description: User object with token
    400:
      description: Invalid input | MISSING_INPUT_KEYS | USER_NOT_FOUND | INCORRECT_PASSWORD
   '''
    user_id = get_user_identity()
    user = User.find_user_by_id(user_id)
    if not user:
        return jsonify({"response" : "USER_NOT_FOUND"}), 400
    if not Utils.check_required_keys_present(request.json, ["title"]):
        return jsonify({"response": "MISSING_INPUT_KEYS"}), 400

    title = request.json["title"]
    description = request.json["description"]
    completed = request.json["completed"]

    project = Project(
        title = title,
        description = description,
        completed = completed
    )

    project.save()

    return jsonify({"response" : "Success"}), 200

