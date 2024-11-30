from flask import Blueprint, request
from ..services.user_wallet_service import (
    setup_user_wallet_service,
    update_user_wallet_service,
    get_user_coins_service
)

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/setupWallet/<userId>', methods=['POST'])
def setup_user_wallet(userId):
    return setup_user_wallet_service(userId)


@wallet_bp.route('/updateWallet/<userId>', methods=['PUT'])
def update_user_wallet(userId):
    data = request.get_json()
    pizzasBought = data.get('pizzasBought', 0)
    return update_user_wallet_service(userId, pizzasBought)


@wallet_bp.route('/getUserCoins/<userId>', methods=['GET'])
def get_user_coins(userId):
    return get_user_coins_service(userId)
