from flask import jsonify, current_app
from ..models.user_wallet import create_wallet, update_wallet
from ..constants import PIZZA_COST


def setup_user_wallet_service(userId):
    try:
        user_ref = current_app.db.collection('users').document(userId)
        user_doc = user_ref.get()

        if(user_doc.exists):
            user_wallet_ref = current_app.db.collection('user_wallets').document()
            user_wallet_data = create_wallet(userId, user_wallet_ref)
            user_wallet_ref.set(user_wallet_data)

            return jsonify({"message": "User Wallet created successfully", "user wallet": user_wallet_data}), 201

        return jsonify({"message": "User not present, wallet not created!"}), 500

    except Exception as e:
        print(f"Error creating wallet: {e}")
        return jsonify({"error": "Error creating wallet"}), 500


def update_user_wallet_service(userId, pizzasBought):
    try:
        wallet_query = current_app.db.collection('user_wallets').where("userId", "==", userId).limit(1).stream()
        wallet_doc = next(wallet_query, None)

        if wallet_doc is None:
            return jsonify({"error": "Wallet not found for user"}), 404
        
        wallet_data = wallet_doc.to_dict()
        total_cost = pizzasBought * PIZZA_COST
        if wallet_data["coinBalance"] < total_cost:
            return jsonify({"error": "Insufficient coin balance"}), 400

        wallet_ref = wallet_doc.reference
        wallet_ref.update({
            "coinBalance": firestore.Increment(-total_cost)
        })

        return jsonify({"message": "User Wallet updated successfully", "new_balance": updated_balance}), 200

    except Exception as e:
        print(f"Error updating wallet: {e}")
        return jsonify({"error": "Error updating wallet"}), 500


def get_user_coins_service(userId):
    try:
        wallet_query = current_app.db.collection('user_wallets').where("userId", "==", userId).limit(1).stream()
        wallet_doc = next(wallet_query, None)
        print(wallet_doc.to_dict())

        if wallet_doc is None:
            return jsonify({"error": "Wallet not found for user"}), 404
        
        current_balance = wallet_doc.to_dict().get("coinBalance")
        return jsonify({"message": "User Wallet fetched successfully", "balance": current_balance}), 200

    except Exception as e:
        print(f"Error fetching wallet: {e}")
        return jsonify({"error": "Error fetching wallet"}), 500