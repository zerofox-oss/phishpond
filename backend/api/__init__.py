from fastapi import (
    FastAPI,
    File,
    UploadFile
)
from . import config

settings = config.Settings()
app = FastAPI()

@app.post("/analyze")
async def analyze(file: bytes = File(...)):
    return {"file_size": len(file)}
