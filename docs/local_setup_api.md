# Local Development Setup Guide

This guide will walk you through setting up the API service for local development. While docker-compose should be maintained and used for demonstration, here is how to run a venv local setup to work specifically with the api.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- MongoDB Atlas account (This is already set up)
- Git

## Setting Up the Virtual Environment

A virtual environment isolates your project dependencies from other Python projects.

### Windows

```bash
# Navigate to the API directory
cd path\to\project\api

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

### macOS/Linux

```bash
# Navigate to the API directory
cd path/to/project/api

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

You'll know the virtual environment is active when you see `(venv)` at the beginning of your command prompt.

## Installing Dependencies

With your virtual environment activated, install the project dependencies:

```bash
# Install all required packages
pip install -r requirements.txt

# If you need to add new packages during development
pip install new-package-name

# Update requirements.txt after adding new packages
pip freeze > requirements.txt
```

## Environment Variable Setup

The API service requires certain environment variables to run properly.

1. Create a `.env` file in the `api` directory:

```bash
touch .env  # or create through your text editor
```

2. Make sure you have an updated `.env` file in /api. Check with the Discord Channel:

```
# MongoDB Connection
MONGODB_URI=mongodb+srv://username:password@cluster-name.mongodb.net/
MONGODB_DB_NAME=your_database_name

# API Configuration
API_PORT=5000
```

**Important Notes:**
- Never commit your `.env` file to version control
- If your password contains special characters (like @, %, etc.), they will be automatically URL-encoded
- Ask a team member for the correct connection string if you're unsure

## Running the API Locally

With everything set up, you can now run the API:

```bash
# Make sure your virtual environment is activated
# (venv) should appear in your command prompt

# Run the API with auto-reload for development
uvicorn app.main:app --reload --port 5000
```

You should see output similar to:
```
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000
```

## Testing Your Setup

You can verify your setup by:

1. Opening a web browser and navigating to [http://localhost:5000/docs](http://localhost:5000/docs)
2. Using curl to test the API: `curl http://localhost:5000/`
3. Checking the terminal logs for successful database connection

## Troubleshooting

### Connection Issues

If you encounter MongoDB connection issues:

1. **Invalid URI format**: Ensure your MongoDB URI is correct and properly formatted
2. **Authentication failed**: Verify your username and password
3. **Network access**: Make sure your IP address is whitelisted in MongoDB Atlas

### Package Issues

If you encounter issues with dependencies:

1. Make sure your virtual environment is activated
2. Update pip: `pip install --upgrade pip`
3. Try reinstalling requirements: `pip install -r requirements.txt --force-reinstall`

### Environment Variable Issues

If environment variables aren't loading:

1. Verify your `.env` file is in the correct location
2. Check for typos in variable names
3. Try loading them manually for testing: `export MONGODB_URI=your_uri`

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

## Getting Help

If you encounter issues not covered in this guide, please reach out to the team lead or post in the team's communication channel.

