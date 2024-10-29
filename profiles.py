# Import collections from the database configuration
from db import personal_data_collection, notes_collection

def get_values(_id):
    """
    Generate default values for a new user profile.

    Args:
        _id: Unique identifier for the user

    Returns:
        dict: Default profile structure with initial values
    """
    return {
        "_id": _id,                         # Unique identifier for the profile
        "general": {
            "name": "",                     # User's full name (empty by default)
            "age": 30,                      # Default age
            "gender": "Male",               # Default gender
            "height": 72,                   # Default height in inches
            "weight": 200,                  # Default weight in pounds
            "activity_level": "Moderately Active"  # Default activity level
        },
        "goals": ["Muscle Gain"],          # Default fitness goals
        "nutrition": {
            "calories": 2000,              # Default daily calorie target
            "protein": 50,                 # Default protein in grams
            "fat": 50,                     # Default fat in grams
            "carbs": 100                   # Default carbs in grams
        }
    }

def create_profile(_id):
    """
    Create a new user profile in the database.

    Args:
        _id: Unique identifier for the user

    Returns:
        tuple: (inserted_id, insert_result)
    """
    # Get default profile values
    profile_values = get_values(_id)
    # Insert the new profile into the database
    result = personal_data_collection.insert_one(profile_values)
    return result.inserted_id, result

def get_profile(_id):
    """
    Retrieve a user's profile from the database.

    Args:
        _id: Unique identifier for the user

    Returns:
        dict: User's profile document or None if not found
    """
    # Query the database for the profile matching the ID
    profile = personal_data_collection.find_one({"_id":{"$eq": _id}})
    return profile

def get_notes(_id):
    """
    Retrieve all notes associated with a user.

    Args:
        _id: Unique identifier for the user

    Returns:
        list: All notes belonging to the user
    """
    # Query the database for all notes matching the user ID
    return list(notes_collection.find({"user_id":{"$eq": _id}}))