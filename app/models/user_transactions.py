from datetime import datetime
from enum import Enum


class UserAction(Enum):
    PIZZA_BOUGHT = "pizzaBought"
    PIZZA_LOGGED = "pizzaLogged"


def create_transaction_data(data, transaction_ref):
    return {
        "transactionId": transaction_ref.id,
        "userId": data["userId"],
        "userAction": UserAction[data["userAction"].upper()].value,
        "numberOfPizzas": int(data["numberOfPizzas"]),
        "timestamp": datetime.utcnow(),
    }


# Function to update an existing transaction document (if needed)
def update_transaction_data(data, doc):
    existing_data = doc.to_dict()
    return {
        "userAction": data.get("userAction", existing_data["userAction"]),
        "numberOfPizzas": int(data.get("numberOfPizzas", existing_data["numberOfPizzas"])),
        "timestamp": datetime.utcnow(),
    }

