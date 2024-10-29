# Import required libraries
from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration constants
ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

# Cache the database connection to prevent multiple connections
@st.cache_resource
def get_db():
    """
    Create and return a database connection.
    Uses Streamlit caching to reuse the connection across reruns.
    """
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db


# Initialize database connection
db = get_db()

# Define collections to be created/used
collection_names = ["personal_data", "notes"]

# Create collections if they don't exist
for collection_name in collection_names:
    try:
        db.create_collection(collection_name)
        print(f"Collection {collection_name} created successfully.")
    except Exception:
        print(f"Collection {collection_name} already exists.")
        pass


# Get references to specific collections for easier access
personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")


