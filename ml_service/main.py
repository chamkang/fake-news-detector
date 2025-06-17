"""FastAPI application for fake image detection."""
import io
import os
from typing import Dict, Any

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from dotenv import load_dotenv
from model import ImageClassifier

# Load environment variables
load_dotenv()

app = FastAPI(title="Fake Image Detection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fake-news-detector-ai.windsurf.build", "http://localhost:5173"],  # Production and development URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the model
model = ImageClassifier()

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Fake Image Detection API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict if an image is fake or real."""
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get prediction
        prediction = model.predict(image)
        
        return {
            "filename": file.filename,
            "prediction": prediction,
            "status": "success"
        }
    except (IOError, Image.UnidentifiedImageError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', '5000'))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
