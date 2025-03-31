# API Routes

## API Endpoints Used by Dashboard
- Get all Prompts - /prompts
- Get all Attacks - /prompts/attacks
- Get all Clean Prompts - /prompts/clean
- Get Attack by Type - /prompts/type?type=whateverattackyoupick ex(prompt-injection)

## Reminder - about running it without Docker
Make sure the api server is running either through the entire docker project
or as an independent component.

### Set up the virtual environment 
if you haven't already set up a virtual environment for the api. 

cd into cyberproject/api
```
python -m venv venv
```

### Start the venv
```
venv/Scripts/activate
```

#### Double Check Requirements
```
pip install -r requirements.txt
```

#### Run
```
uvicorn app.main:app --reload --port 5000
```

point your browser to localhost:5000/prompts and you should see a json object with all th prompts in the db


