from flask import Blueprint, request
from ..services.user_service import create_user_service, get_users_service, get_user_service, update_user_service, delete_user_service, get_users_by_filter_service, get_available_pizzas_for_logging_service

user_bp = Blueprint('user', __name__)

@user_bp.route('/createUser', methods=['POST'])
def create_user():
    return create_user_service(request)

@user_bp.route('/getUsers', methods=['GET'])
def get_users():
    return get_users_service()

@user_bp.route('/getUser/<userId>', methods=['GET'])
def get_user(userId):
    return get_user_service(userId)

@user_bp.route('/updateUser/<userId>', methods=['PUT'])
def update_user(userId):
    return update_user_service(userId, request)

@user_bp.route('/deleteUser/<userId>', methods=['DELETE'])
def delete_user(userId):
    return delete_user_service(userId)

@user_bp.route('/getUsersByFilter', methods=['POST'])
def get_users_by_filter():
    return get_users_by_filter_service(request)

@user_bp.route('/getAvailablePizzasForLogging/<userId>', methods=['GET'])
def get_available_pizzas_for_logging(userId):
    return get_available_pizzas_for_logging_service(userId)
