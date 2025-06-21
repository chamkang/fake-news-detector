"""FastAPI application for fake image detection."""
import io
import os
import sys
from typing import Dict, Any, Optional
import requests
import traceback
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
from dotenv import load_dotenv
from model import ImageClassifier

# Load environment variables
load_dotenv()

app = FastAPI(title="Fake Image Detection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://verifact-image-detector.windsurf.build",
        "http://localhost:5173",
        "https://verifact-image-detector.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Initialize the model
model = ImageClassifier()

@app.get("/")
def root():
    return {"status": "ok", "message": "VeriFact API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "verifact-api"}

@app.post("/predict")
async def predict(file: Optional[UploadFile] = File(None), url: Optional[str] = Form(None)):
    logging.info("Received prediction request")
    if file:
        logging.info(f"File upload: {file.filename}")
    if url:
        logging.info(f"URL: {url}")
    """Predict if an image is fake or real."""
    try:
        if file:
            # Read image file
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            source = file.filename
        elif url:
            # Download image from URL
            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            source = url
        else:
            return JSONResponse(
                status_code=400,
                content={"detail": "Either file or url must be provided"}
            )

        # Get prediction
        try:
            prediction, confidence = model.predict(image)
            
            return JSONResponse({
                "source": source,
                "prediction": prediction,
                "confidence": confidence,
                "status": "success",
                "detail": f"Image analyzed successfully"
            })
        except Exception as model_error:
            print(f"Model prediction error: {str(model_error)}")
            print(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={"detail": "Error analyzing image. Please try again."}
            )
            
    except requests.exceptions.RequestException as e:
        print(f"URL download error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": f"Error downloading image: {str(e)}"}
        )
    except (IOError, Image.UnidentifiedImageError) as e:
        print(f"Image processing error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": f"Invalid image file: {str(e)}"}
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error. Please try again."}
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', '8080'))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
