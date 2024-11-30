from datetime import datetime
from ..constants import COINS_ASSIGNED_TO_USERS

def create_wallet(userId, user_ref):
    return{
        "walletId": user_ref.id,
        "userId": userId,
        "coinBalance": COINS_ASSIGNED_TO_USERS
    }

def update_wallet(coinBalance):
    return{
        "coinBalance": coinBalance
    }