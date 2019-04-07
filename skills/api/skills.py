from skills.api.validations import validate_skill_json, validate_category_json, validate_new_skill_name, \
    validate_new_category_name
from skills.models import Skill, Category, User, to_collection_dict
from skills.api.errors import error_response, bad_request
from flask import jsonify, request, url_for
from config import ErrorMessages, Config
from skills.api import bp


@bp.route('/skills', methods=['GET'])
def get_skills():
    response = User.check_token(request)
    if response == 200:
        return jsonify(to_collection_dict(Skill))
    return error_response(response)


@bp.route('/skills', methods=['POST'])
def create_skill():
    response = User.check_token(request)
    if response == 200 \
            and User.query.filter_by(token=request.headers.get('Authorization')).first().email == Config.ADMIN_EMAIL:
        data = request.get_json() or {}
        if not validate_skill_json(data):
            return bad_request(ErrorMessages.API_FORMAT_NOT_ALLOWED)
        if not validate_new_skill_name(data['skill_name']):
            return bad_request(ErrorMessages.API_SKILL_NAME_ERROR)
        if not validate_new_category_name(data['category_name']):
            return bad_request(ErrorMessages.API_CATEGORY_NAME_ERROR)
        if Skill.insert_new_skill(data['skill_name'], data['category_name'], data.get('is_shown', 1)):
            response = jsonify(Skill.query.filter_by(skill_name=data['skill_name']).first().to_dict('name'))
            response.status_code = 201
            response.headers['Location'] = url_for('api.get_skill_by_name', skill_name=data['skill_name'])
            return response
        else:
            return bad_request(ErrorMessages.API_SKILL_INSERT_ERROR)
    return error_response(response if response != 200 else 401)


@bp.route('/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill_by_id(skill_id):
    response = User.check_token(request)
    if response == 200 \
            and User.query.filter_by(token=request.headers.get('Authorization')).first().email == Config.ADMIN_EMAIL:
        skill_to_be_deleted = Skill.query.filter_by(id_skill=skill_id).first()
        if skill_to_be_deleted is None:
            return bad_request(ErrorMessages.API_DELETE_SKILL_FAILURE)
        if Skill.delete_skill(skill_to_be_deleted.skill_name):
            response = jsonify(Config.API_DELETION_SUCCESS)
            response.status_code = 200
            return response
        else:
            return bad_request(ErrorMessages.API_DELETE_SKILL_FAILURE)
    return error_response(response if response != 200 else 401)


@bp.route('/skills/<string:skill_name>', methods=['DELETE'])
def delete_skill_by_name(skill_name):
    response = User.check_token(request)
    if response == 200 \
            and User.query.filter_by(token=request.headers.get('Authorization')).first().email == Config.ADMIN_EMAIL:
        skill_to_be_deleted = Skill.query.filter_by(skill_name=skill_name).first()
        if skill_to_be_deleted is None:
            return bad_request(ErrorMessages.API_DELETE_SKILL_FAILURE)
        if Skill.delete_skill(skill_to_be_deleted.skill_name):
            response = jsonify(Config.API_DELETION_SUCCESS)
            response.status_code = 200
            return response
        else:
            return bad_request(ErrorMessages.API_DELETE_SKILL_FAILURE)
    return error_response(response if response != 200 else 401)


@bp.route('/skills/<string:skill_name>', methods=['GET'])
def get_skill_by_name(skill_name):
    response = User.check_token(request)
    if response == 200:
        return jsonify(Skill.query.filter_by(skill_name=skill_name).first_or_404().to_dict('name'))
    return error_response(response)


@bp.route('/skills/<int:skill_id>', methods=['GET'])
def get_skill_by_id(skill_id):
    response = User.check_token(request)
    if response == 200:
        return jsonify(Skill.query.filter_by(id_skill=skill_id).first_or_404().to_dict('id'))
    return error_response(response)


@bp.route('/categories', methods=['GET'])
def get_categories():
    response = User.check_token(request)
    if response == 200:
        return jsonify(to_collection_dict(Category))
    return error_response(response)


@bp.route('/categories', methods=['POST'])
def create_category():
    response = User.check_token(request)
    if response == 200 \
            and User.query.filter_by(token=request.headers.get('Authorization')).first().email == Config.ADMIN_EMAIL:
        data = request.get_json() or {}
        if not validate_category_json(data):
            return bad_request(ErrorMessages.API_FORMAT_NOT_ALLOWED)
        if not validate_new_category_name(data['category_name']):
            return bad_request(ErrorMessages.API_CATEGORY_NAME_ERROR)
        if Category.insert_new_category(data['category_name'], data.get('is_shown', 1)):
            response = jsonify(Category.query.filter_by(category_name=data['category_name']).first().to_dict('name'))
            response.status_code = 201
            response.headers['Location'] = url_for('api.get_category_by_name', category_name=data['category_name'])
            return response
        else:
            return bad_request(ErrorMessages.API_CATEGORY_INSERT_ERROR)
    return error_response(response if response != 200 else 401)


@bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category_by_id(category_id):
    response = User.check_token(request)
    if response == 200 \
            and User.query.filter_by(token=request.headers.get('Authorization')).first().email == Config.ADMIN_EMAIL:
        category_to_be_deleted = Category.query.filter_by(id_skill_cat=category_id).first()
        if category_to_be_deleted is None:
            return bad_request(ErrorMessages.API_DELETE_CATEGORY_FAILURE)
        if Category.delete_category(category_to_be_deleted.category_name):
            response = jsonify(Config.API_DELETION_SUCCESS)
            response.status_code = 200
            return response
        else:
            return bad_request(ErrorMessages.API_DELETE_CATEGORY_FAILURE)
    return error_response(response if response != 200 else 401)


@bp.route('/categories/<string:category_name>', methods=['DELETE'])
def delete_category_by_name(category_name):
    response = User.check_token(request)
    if response == 200 \
            and User.query.filter_by(token=request.headers.get('Authorization')).first().email == Config.ADMIN_EMAIL:
        if Category.delete_category(category_name):
            response = jsonify(Config.API_DELETION_SUCCESS)
            response.status_code = 200
            return response
        else:
            return bad_request(ErrorMessages.API_DELETE_CATEGORY_FAILURE)
    return error_response(response if response != 200 else 401)


@bp.route('/categories/<string:category_name>', methods=['GET'])
def get_category_by_name(category_name):
    response = User.check_token(request)
    if response == 200:
        return jsonify(Category.query.filter_by(category_name=category_name).first_or_404().to_dict('name'))
    return error_response(response)


@bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    response = User.check_token(request)
    if response == 200:
        return jsonify(Category.query.filter_by(id_skill_cat=category_id).first_or_404().to_dict('id'))
    return error_response(response)
