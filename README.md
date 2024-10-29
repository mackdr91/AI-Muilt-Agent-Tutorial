# Personal Fitness App

A Streamlit-based personal fitness application that allows users to:

- Create and manage personal profiles
- Track personal data (name, age, gender, height, weight)
- Set activity levels
- Get personalized fitness recommendations
- Add and manage notes

## Features

- User profile management
- Personal data form with various inputs
- Activity level tracking
- AI-powered recommendations (via ai.py)
- Note-taking functionality

## Technical Stack

- Streamlit for the web interface
- Python backend
- AI integration for personalized recommendations
- LangFlow for workflow automation
- Astra DB for data storage
- OpenAI for intelligent features

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/personal-fitness-app.git
cd personal-fitness-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_openai_api_key
ASTRA_DB_TOKEN=your_astra_db_token
ASTRA_DB_ID=your_astra_db_id
```

## Running the Application

1. Ensure your virtual environment is activated
2. Run the Streamlit application:
```bash
streamlit run main.py
```
3. Open your browser and navigate to `http://localhost:8501`

## Development Setup

To contribute to the project:

1. Fork the repository
2. Create a new branch for your feature
3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```
4. Make your changes and submit a pull request
