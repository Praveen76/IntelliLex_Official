
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root  = file.parent, file.parents[1]
sys.path.append(str(root))
import logging

print("parent :",parent)
print("root :",root)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

import os
# print("Current directory:", os.getcwd())

# import sys
# print("\n".join(sys.path))

# In main.py
# try:
#     import intlx_model.Utils  # Test if this basic import works
#     print("Module import successful")
# except ImportError as e:
#     print("Error importing module:", str(e))

# from intlx_model import __version__ as _version
# from intlx_model.config.core import config
print("Will import modulesin main file")
from intlx_model.predict import predict_resp
from intlx_model.Utils import local_vectordb_path, get_openai_api_key
print("Imported modules in main file")


# Store OpenAI key (initialized during startup)
openai_key = None
# Load OpenAI key from Secrets Manager
openai_key = get_openai_api_key()
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
    logging.info("OpenAI API key loaded and set in environment.")
else:
    raise ValueError("OpenAI API key could not be retrieved.")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout),
              logging.StreamHandler(sys.stderr),  # Ensure stderr is captured
             ]
)

class PredictRequest(BaseModel):
    """
    You can define a Pydantic model for request validation.
    Adjust as necessary for your data structure.
    """
    text: str
    # isBase64Encoded: bool = False
    # body: str = ""  # Optional, in case you are using the base64-encoded approach

print("Will create app now")
# Create FastAPI instance
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        logging.info("Loading OpenAI API key from AWS Secrets Manager...")
        openai_key = get_openai_api_key()
        if not openai_key:
            raise ValueError("OpenAI API key could not be retrieved.")
        os.environ["OPENAI_API_KEY"] = openai_key
        logging.info("OpenAI API key successfully loaded.")
    except Exception as e:
        logging.error(f"Failed to load OpenAI API key: {e}")
        raise RuntimeError("Application cannot start without a valid OpenAI API key.")
    
    yield  # This point allows the application to run

    # Shutdown logic (if any)
    logging.info("Application is shutting down...")

from fastapi.responses import JSONResponse

@app.get("/")
async def health_check():
    """
    A simple health check endpoint.
    """
    return JSONResponse(content={"message": "Service is up and running."}, status_code=200)


@app.post("/predict")
async def predict(payload: PredictRequest):
    """
    Endpoint to accept a JSON body using the PredictRequest model.
    """
    try:
        logging.info("Incoming request to /predict")
        print("predict func started")
        logging.info(f"Payload: {payload}") 
        
        # Use only the `text` field
        incoming_msg = payload.text.strip()
        print("incoming_msg :", incoming_msg, flush=True)
        if not incoming_msg:
            logging.warning("No text provided in the request.")
            raise HTTPException(status_code=400, detail="The 'text' field cannot be empty.")

        logging.info(f"Received text: {incoming_msg}")
        print(f"Received text: {incoming_msg}")

        responses = predict_resp(incoming_msg, local_vectordb_path)
        logging.info(f"Responses: {responses}")
        print(f"Responses: {responses}")

        return {"responses": responses}

    except HTTPException as he:
        logging.error(f"HTTP error occurred: {he.detail}")
        raise he
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True, log_level="debug")



