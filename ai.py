import json
from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import requests
from typing import Optional
import os

# Load environment variables from .env file
load_dotenv()

# API Configuration Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "5e9368ca-35c9-4fa3-8728-2a93725018e8"
APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")


def dict_to_string(obj, level=0):
    """
    Recursively converts a nested dict or list into a string representation.

    Args:
        obj: The object to convert to a string.
        level: The indentation level, used to format nested objects.

    Returns:
        A string representation of the object.

    Example:
        >>> dict_to_string({"a": 1, "b": {"x": "y", "z": 3}})
        "a: 1, b: x: y, z: 3"
    """
    strings = []
    indent = "  " * level
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx+1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")
    return ", ".join(strings)

def ask_ai(profile, question):
    """
    Send a question to the AI along with a user profile for context.

    Args:
        profile (dict): User profile containing relevant information
        question (str): The question to ask the AI

    Returns:
        str: AI's response to the question
    """
    # Configure input values for the AI model
    TWEAKS = {
        "TextInput-ymppr": {
            "input_value": question
        },
        "TextInput-wmXQ8": {
            "input_value": dict_to_string(profile)
        },
    }

    # Run the AI flow and extract the response
    result = run_flow_from_json(
        flow="AskAIv2.json",
        input_value="message",
        fallback_to_env_vars=True,
        tweaks=TWEAKS
    )

    return result[0].outputs[0].results['text'].data['text']

def get_macros(profile, goals):
    """
    Generate macro recommendations based on user profile and fitness goals.

    Args:
        profile (dict): User profile containing relevant information
        goals (list): List of fitness goals

    Returns:
        dict: Recommended macros and nutritional information
    """
    TWEAKS = {
        "TextInput-1l5Zk": {
            "input_value": ", ".join(goals)
        },
        "TextInput-S9eso": {
            "input_value": dict_to_string(profile)
        },
    }

    return run_flow("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)

def run_flow(message: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    """
    Execute a Langflow workflow with the specified parameters.

    Args:
        message (str): Input message for the flow
        output_type (str): Type of output expected (default: "chat")
        input_type (str): Type of input provided (default: "chat")
        tweaks (dict, optional): Modifications to the flow's default behavior
        application_token (str, optional): Authentication token for the API

    Returns:
        dict: Processed response from the Langflow API
    """
    # Construct API endpoint URL
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macros"

    # Prepare request payload
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }

    # Set up authentication headers if token provided
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}

    # Make API request and parse response
    response = requests.post(api_url, json=payload, headers=headers)

    return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])

