from flask import Blueprint, request, jsonify
from ..constants import PIZZA_COST

config_bp = Blueprint('config', __name__)

@config_bp.route('/getConfigs', methods=['GET'])
def create_user():
    return jsonify({"pizzaCost": PIZZA_COST}), 200
