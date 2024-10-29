from db import personal_data_collection, notes_collection
from datetime import datetime

def update_personal_data(existing_data, updated_type, **kwargs):
    if updated_type == "goals":
        existing_data["goals"] = kwargs.get("goals", [])
        updated_field = {
            "goals": existing_data["goals"]
        }
    else:
        existing_data[updated_type] = kwargs
        updated_field = {
            updated_type: existing_data[updated_type]
        }
    personal_data_collection.update_one({"_id": existing_data["_id"]}, {"$set": updated_field})

    return existing_data


def add_note(note, profile_id):
    new_note = {
        "user_id": profile_id,
        "text": note,
        "$vectorize": note,
        "metadata": {
            "injested": datetime.now()
        }
    }

    result = notes_collection.insert_one(new_note)
    new_note["_id"] = result.inserted_id
    return new_note


def delete_note(_id):
    notes_collection.delete_one({"_id": _id})