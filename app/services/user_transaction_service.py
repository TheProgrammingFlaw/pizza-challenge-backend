from firebase_admin import firestore
from flask import request, jsonify
from datetime import datetime
from ..constants import PIZZA_COST
from ..socket_config import socketio

db = firestore.client()
transactions_collection = db.collection('user_transactions')
users_collection = db.collection('users')
wallets_collection = db.collection('user_wallets')

def buy_pizza_transaction(request):
    try:
        data = request.get_json()
        userId = data["userId"]
        number_of_pizzas = int(data["numberOfPizzas"])

        wallet_query = wallets_collection.where("userId", "==", userId).limit(1).stream()
        wallet_doc = next(wallet_query, None)

        if wallet_doc is None:
            return jsonify({"error": "Wallet not found for user"}), 404
        
        wallet_data = wallet_doc.to_dict()

        total_cost = number_of_pizzas * PIZZA_COST

        # Check if the user has enough coinBalance
        if wallet_data["coinBalance"] < total_cost:
            return jsonify({"error": "Insufficient coin balance"}), 400

        wallet_ref = wallet_doc.reference
        # Deduct coin balance
        wallet_ref.update({
            "coinBalance": firestore.Increment(-total_cost)
        })

        user_doc_ref = users_collection.document(userId)
        user_doc = user_doc_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict()
        total_bought = user_data.get("totalPizzasBought", 0) + number_of_pizzas

        user_doc_ref.update({
            "totalPizzasBought": firestore.Increment(number_of_pizzas)
        })

        transaction_ref = transactions_collection.document()
        transaction_data = {
            "transactionId": transaction_ref.id,
            "userId": data["userId"],
            "userAction": "pizzaBought",
            "numberOfPizzas": int(data["numberOfPizzas"]),
            "timestamp": datetime.utcnow(),
        }

        transaction_ref.set(transaction_data)

        return jsonify({"message": "Transaction created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400



def log_pizza_transaction(request):
    try:
        data = request.get_json()
        userId = data["userId"]
        number_of_pizzas = int(data["numberOfPizzas"])

        user_doc_ref = users_collection.document(userId)
        user_doc = user_doc_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict()
        total_bought = user_data.get("totalPizzasBought", 0)
        total_logged = user_data.get("totalPizzasLogged", 0)
        available_to_log = max(0, total_bought - total_logged)

        # Check if there are enough pizzas left to log
        if available_to_log < number_of_pizzas:
            return jsonify({"error": f"Not enough pizzas to log. You can only log {available_to_log} more pizzas."}), 400

        # Log the pizzas by updating the totalPizzasLogged
        user_doc_ref.update({
            "totalPizzasLogged": firestore.Increment(number_of_pizzas)
        })

        # Create a transaction log entry
        transaction_ref = transactions_collection.document()
        transaction_data = {
            "transactionId": transaction_ref.id,
            "userId": userId,
            "userAction": "pizzaLogged",
            "numberOfPizzas": number_of_pizzas,
            "timestamp": datetime.utcnow(),
        }
        transaction_ref.set(transaction_data)

        updated_user_data = {
            "userId": userId,
            "totalPizzasLogged": total_logged + number_of_pizzas,
            "availableToLog": available_to_log - number_of_pizzas,
        }
        socketio.emit('user_update', {'message': f"{number_of_pizzas} pizzas logged", 'user': updated_user_data})

        return jsonify({"message": f"{number_of_pizzas} pizzas logged successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_transactions_service():
    try:
        transactions = [doc.to_dict() for doc in transactions_collection.stream()]
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_transaction_service(transactionId):
    try:
        transaction_doc = transactions_collection.document(transactionId).get()
        if transaction_doc.exists:
            return jsonify(transaction_doc.to_dict()), 200
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def update_transaction_service(transactionId, request):
    try:
        data = request.get_json()
        transaction_ref = transactions_collection.document(transactionId)
        transaction_doc = transaction_ref.get()

        if transaction_doc.exists:
            updated_data = {
                "userAction": data.get("userAction", transaction_doc.to_dict()["userAction"]),
                "numberOfPizzas": int(data.get("numberOfPizzas", transaction_doc.to_dict()["numberOfPizzas"])),
                "timestamp": datetime.utcnow(),
            }
            transaction_ref.update(updated_data)
            return jsonify({"message": "Transaction updated successfully"}), 200
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def delete_transaction_service(transactionId):
    try:
        transaction_ref = transactions_collection.document(transactionId)
        transaction_doc = transaction_ref.get()
        if transaction_doc.exists:
            transaction_ref.delete()
            return jsonify({"message": "Transaction deleted successfully"}), 200
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_transactions_by_filter_service(request):
    try:
        data = request.get_json()
        query = transactions_collection

        # Apply filters based on user input
        if "userId" in data:
            query = query.where("userId", "==", data["userId"])
        if "userAction" in data:
            query = query.where("userAction", "==", data["userAction"])
        if "startDate" in data and "endDate" in data:
            start_date = datetime.fromisoformat(data["startDate"])
            end_date = datetime.fromisoformat(data["endDate"])
            query = query.where("timestamp", ">=", start_date).where("timestamp", "<=", end_date)

        transactions = [doc.to_dict() for doc in query.stream()]
        sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'], reverse=True)
        return jsonify(sorted_transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
