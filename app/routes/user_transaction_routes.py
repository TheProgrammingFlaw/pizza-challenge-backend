from flask import Blueprint, request, jsonify
from ..services.user_transaction_service import (
    buy_pizza_transaction,
    log_pizza_transaction,
    get_transactions_service,
    get_transaction_service,
    update_transaction_service,
    delete_transaction_service,
    get_transactions_by_filter_service
)

# Define Blueprint for user transactions
transaction_bp = Blueprint('transaction', __name__)

# Route to create a new user transaction
@transaction_bp.route('/buyPizza', methods=['POST'])
def create_transaction():
    return buy_pizza_transaction(request)

@transaction_bp.route('/logPizza', methods=['POST'])
def log_pizza():
    return log_pizza_transaction(request)


# Route to get all user transactions
@transaction_bp.route('/getTransactions', methods=['GET'])
def get_transactions():
    return get_transactions_service()

# Route to get a specific user transaction by transaction ID
@transaction_bp.route('/getTransaction/<transactionId>', methods=['GET'])
def get_transaction(transactionId):
    return get_transaction_service(transactionId)

# Route to update a specific user transaction by transaction ID
@transaction_bp.route('/updateTransaction/<transactionId>', methods=['PUT'])
def update_transaction(transactionId):
    return update_transaction_service(transactionId, request)

# Route to delete a specific user transaction by transaction ID
@transaction_bp.route('/deleteTransaction/<transactionId>', methods=['DELETE'])
def delete_transaction(transactionId):
    return delete_transaction_service(transactionId)

# Route to filter user transactions based on various criteria (e.g., userId, userAction, date range, etc.)
@transaction_bp.route('/getTransactionsByFilter', methods=['POST'])
def get_transactions_by_filter():
    return get_transactions_by_filter_service(request)
