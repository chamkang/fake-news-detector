"""Image processing service for fake image detection."""
from io import BytesIO

import cv2
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier
from PIL import Image

class ImageProcessor:
    """Image processor for feature extraction and fake image detection.
    
    This class handles image preprocessing, feature extraction, and classification
    using a Random Forest model. Features include color histograms, edge detection,
    and other image statistics to identify potential manipulations.
    """
    def __init__(self):
        # Initialize model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.image_size = (224, 224)
        self.is_trained = False
        
    def extract_features(self, image_array):
        """Extract basic image features"""
        try:
            # Convert to grayscale
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array

            # Basic feature extraction
            features = []
            
            # Add histogram features
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            features.extend(hist.flatten())
            
            # Add basic statistics
            features.extend([
                np.mean(gray),
                np.std(gray),
                np.max(gray),
                np.min(gray),
            ])
            
            # Add edge detection features
            edges = cv2.Canny(gray, 100, 200)
            features.append(np.mean(edges))
            
            return np.array(features)
            
        except Exception as e:
            raise ValueError(f'Error extracting features: {e}') from e
    
    def train(self, images, labels):
        """Train the model with provided images and labels"""
        try:
            features = []
            for image in images:
                img_features = self.extract_features(image)
                features.append(img_features)
            
            feature_matrix = np.array(features)
            y = np.array(labels)
            
            self.model.fit(feature_matrix, y)
            self.is_trained = True
            
        except Exception as e:
            raise ValueError(f'Error training model: {e}') from e
    
    def preprocess_image(self, image_data):
        """Preprocess image for feature extraction"""
        try:
            # Convert bytes to image
            image = Image.open(BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to expected dimensions
            image = image.resize(self.image_size)
            
            # Convert to numpy array
            img_array = np.array(image)
            
            return img_array
            
        except Exception as e:
            raise ValueError(f'Error preprocessing image: {e}') from e
    
    def download_image(self, url):
        """Download image from URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise ValueError(f'Error downloading image: {e}') from e
    
    def analyze(self, image_data):
        """Analyze image for potential manipulation"""
        try:
            if not self.is_trained:
                # Return a random prediction for demonstration
                # In production, you should train the model first
                is_fake = bool(np.random.randint(2))
                confidence = np.random.uniform(0.6, 0.9)
                return {
                    'is_fake': is_fake,
                    'confidence': float(confidence)
                }
            
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            
            # Extract features
            features = self.extract_features(processed_image)
            
            # Get prediction
            prediction = self.model.predict_proba([features])[0]
            is_fake = bool(prediction[1] > 0.5)
            confidence = float(max(prediction))
            
            return {
                'is_fake': is_fake,
                'confidence': confidence
            }
            
        except Exception as e:
            raise ValueError(f'Error analyzing image: {e}') from e
