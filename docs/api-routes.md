# API Routes

## API Endpoints Used by Dashboard
- Get all Prompts - /prompts
- Get all Attacks - /prompts/attacks
- Get all Clean Prompts - /prompts/clean
- Get Attack by Type - /prompts/type?=whateverattackyoupick

## Note
Make sure the api server is running either through the entire docker project
or as an independent component.

#### Double Check Requirements
```
pip install -r requirements.txt
```

#### Run
```
uvicorn app.main:app --reload --port 5000
```


