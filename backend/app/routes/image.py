from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from ..services.image_processor import ImageProcessor
from ..services.metadata_extractor import MetadataExtractor

image_bp = Blueprint('image', __name__)
image_processor = ImageProcessor()
metadata_extractor = MetadataExtractor()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route('/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files and 'url' not in request.form:
        return jsonify({'error': 'No file or URL provided'}), 400

    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            # Process uploaded file
            image_data = file.read()
            
        else:
            # Process URL
            url = request.form['url']
            image_data = image_processor.download_image(url)

        # Extract metadata
        metadata = metadata_extractor.extract(image_data)
        
        # Analyze image for fakeness
        prediction = image_processor.analyze(image_data)
        
        return jsonify({
            'result': {
                'is_fake': prediction['is_fake'],
                'confidence': prediction['confidence'],
                'metadata': metadata
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
