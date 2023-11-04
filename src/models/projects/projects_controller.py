from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required

from src.common.jwt_helper import create_token_obj_bundle, get_user_identity
from src.common.utils import Utils
from src.models.projects.project import Project
from src.models.users.user import User

projects_blueprint = Blueprint("projects", __name__)


@projects_blueprint.route("/create", methods=["POST"])
@jwt_required()
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
      description: Success message
    400:
      description: Invalid input | MISSING_INPUT_KEYS
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


@projects_blueprint.route("/modify", methods=["POST"])
# @jwt_required()
@expects_json(
    {
    'type': 'object',
    'properties': {
        'project_id' : {'type': 'string'},
        'title': {'type': 'string'},
        'description': {'type': 'string'},
        'completed' : {'type' : 'boolean'}
    },
    'required': ['project_id']
    }
)
def modify_project():
    '''Modify Project
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
         project_id:
           type: "string"
         title:
           type: "string"
         description:
           type: "string"
         completed:
           type: "boolean"
   responses:
    200:
      description: Success message
    400:
      description: Invalid input | MISSING_INPUT_KEYS | PROJECT_NOT_FOUND
   '''
    user_id = get_user_identity()
    user = User.find_user_by_id(user_id)
    if not user:
        return jsonify({"response" : "USER_NOT_FOUND"}), 400
    if not Utils.check_required_keys_present(request.json, ["title"]):
        return jsonify({"response": "MISSING_INPUT_KEYS"}), 400

    project = Project.find_project_by_id(request.json["project_id"])

    if project is None:
        return jsonify({"response": "PROJECT_NOT_FOUND"}), 400

    if "title" in request.json:
        project.title = request.json["title"]
    if "description" in request.json:
        project.description = request.json["description"]
    if "completed" in request.json:
        project.completed = request.json["completed"]

    project.save()

    return jsonify({"response" : "Success"}), 200



@projects_blueprint.route("/delete/<project_id>", methods=["GET"])
@jwt_required()
def delete_project(project_id):
    '''Delete Project
    ---
   tags:
   - "Projects"
   consumes:
   - "application/json"
   security: [ { 'bearerAuth': [] } ]
   parameters:
   - name: project_id
     in: path
     type: string
     required: true

   responses:
    200:
      description: Delete Project
    400:
      description: PROJECT_NOT_FOUND
    '''

    if Project.find_project_by_id(project_id) is None:
        return jsonify({"response": "PROJECT_NOT_FOUND"}), 400

    Project.delete_project_by_id(project_id)
    return jsonify({"response" : "Success"}), 200



@projects_blueprint.route("/get/<project_id>", methods=["GET"])
@jwt_required()
def get_project(project_id):
    '''Get project details
    ---
   tags:
   - "Projects"
   consumes:
   - "application/json"
   security: [ { 'bearerAuth': [] } ]
   parameters:
   - name: project_id
     in: path
     type: string
     required: true

   responses:
    200:
      description: Delete Project
    400:
      description: PROJECT_NOT_FOUND
    '''

    project = Project.find_project_by_id(project_id)
    if Project.find_project_by_id(project_id) is None:
        return jsonify({"response": "PROJECT_NOT_FOUND"}), 400

    return jsonify({k:v for k,v in project.__dict__.items() if not k in ["_sa_instance_state"]}), 200
