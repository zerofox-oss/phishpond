## backend

==

This backend is written in fastapi. Right now, it can only do `/analyze` of a zip file. 

### Run

1. Run `docker-compose up backend` and navigate to `localhost:5000`
2. OR `pip3 install -r requirements.txt && uvicorn backend.main:app --reload --port 5000` 

To test locally with JSON output, run the following cURL command:

`curl -H "Content-Type:multipart/form-data" --form "file=@phishking.zip" -X POST localhost:5000/analyze`
