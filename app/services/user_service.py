from flask import jsonify, current_app
from ..models.user import create_user_data, update_user_data
from .user_wallet_service import setup_user_wallet_service


def create_user_service(request):
    try:
        data = request.json
        if not all(key in data for key in ("name", "age", "gender")):
            return jsonify({"error": "Missing required fields: name, age, or gender"}), 400
        
        user_ref = current_app.db.collection('users').document()
        user_data = create_user_data(data, user_ref)
        user_ref.set(user_data)

        setup_user_wallet_service(user_ref.id)

        return jsonify({"message": "User created successfully", "user": user_data}), 201
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user"}), 500


def get_users_service():
    try:
        users_ref = current_app.db.collection('users')
        query = users_ref.order_by("createdAt").stream()
        users = [doc.to_dict() for doc in query]

        if users:
            return jsonify({"users": users}), 200
        else:
            return jsonify({"message": "No users found"}), 200
    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({"error": "Failed to fetch users"}), 500


def get_user_service(userId):
    try:
        user_ref = current_app.db.collection('users').document(userId)
        doc = user_ref.get()

        if doc.exists:
            return jsonify({"user": doc.to_dict()}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error fetching user: {e}")
        return jsonify({"error": "Failed to fetch user"}), 500


def update_user_service(userId, request):
    try:
        data = request.json
        user_ref = current_app.db.collection('users').document(userId)
        doc = user_ref.get()

        if not doc.exists:
            return jsonify({"message": "User not found"}), 404

        for key, value in doc.to_dict().items():
            print(f"{key}: {value}")
        
        for key, value in data.items():
            print(f"{key}: {value}")

        update_data = update_user_data(data, doc)
        print('update_data : ', update_data)

        ## Implement a Check that only desired details are allowed to be changed
        user_ref.update(update_data)

        return jsonify({"message": "User updated successfully", "user": update_data}), 200
    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({"error": "Failed to update user"}), 500


def delete_user_service(userId):
    try:
        user_ref = current_app.db.collection('users').document(userId)
        doc = user_ref.get()

        if not doc.exists:
            return jsonify({"message": "User not found"}), 404

        user_ref.delete()

        wallet_query = current_app.db.collection('user_wallets').where("userId", "==", userId).limit(1).stream()
        wallet_doc = next(wallet_query, None)
        wallet_ref = wallet_doc.reference
        wallet_ref.delete()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({"error": "Failed to delete user"}), 500


def get_users_by_filter_service(request):
    try:
        data = request.json
        age = data.get("age")
        gender = data.get("gender")

        users_ref = current_app.db.collection('users')
        query = users_ref

        if age:
            query = query.where("age", "==", int(age))

        if gender:
            query = query.where("gender", "==", gender)

        users = [doc.to_dict() for doc in query.stream()]

        if users:
            return jsonify({"users": users}), 200
        else:
            return jsonify({"message": "No users found matching the criteria"}), 200
    except Exception as e:
        print(f"Error fetching users by filter: {e}")
        return jsonify({"error": "Failed to fetch users"}), 500


def get_available_pizzas_for_logging_service(userId):
    try:
        user_doc = current_app.db.collection('users').document(userId).get()
        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404
        
        user_data = user_doc.to_dict()
        total_bought = user_data.get("totalPizzasBought", 0)
        total_logged = user_data.get("totalPizzasLogged", 0)
        available_to_log = max(0, total_bought - total_logged)

        return jsonify({"availableToLog": available_to_log}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400