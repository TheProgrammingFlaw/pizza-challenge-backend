from datetime import datetime


def create_user_data(data, user_ref):
    return {
        "userId": user_ref.id,
        "name": data["name"],
        "age": int(data["age"]),
        "gender": data["gender"],
        "totalPizzasBought": 0,
        "totalPizzasLogged": 0,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

def update_user_data(data, doc):
    return {
        "name": data.get("name", doc.to_dict()["name"]),
        "age": int(data.get("age", doc.to_dict()["age"])),
        "gender": data.get("gender", doc.to_dict()["gender"]),
        "updatedAt": datetime.utcnow()
    }
