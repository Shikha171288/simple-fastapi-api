# main.py
import os
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()

app = FastAPI(title="Secure API Example")

# Get API key from environment
API_KEY = os.getenv("API_KEY")

def verify_api_key(request: Request):
    # Try header first
    key = request.headers.get("X-API-Key")
    if not key:
        # fallback to query param
        key = request.query_params.get("api_key")
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

# Public endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the public API!"}

# Protected endpoint
@app.get("/secret")
def read_secret(api_key: None = Depends(verify_api_key)):
    return {"secret_data": "This is top-secret information!"}
