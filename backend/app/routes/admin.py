"""Admin routes for managing training data and model training."""
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any

from ..models.training_data import TrainingData, SessionLocal
from ..database import db

admin_bp = Blueprint('admin', __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@admin_bp.route('/training-data', methods=['POST'])
def upload_training_data():
    """Upload training data with labels"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    label = request.form.get('label')
    if label not in ['real', 'fake']:
        return jsonify({'error': 'Invalid label. Must be "real" or "fake"'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Save to database
        training_data = TrainingData(
            filename=filename,
            filepath=filepath,
            label=label
        )
        db.session.add(training_data)
        db.session.commit()

        return jsonify({
            'message': 'Training data uploaded successfully',
            'id': training_data.id
        })

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/training-data', methods=['GET'])
def get_training_data():
    """Get list of training data"""
    try:
        training_data = TrainingData.query.all()
        return jsonify({
            'training_data': [
                {
                    'id': data.id,
                    'filename': data.filename,
                    'label': data.label,
                    'created_at': data.created_at.isoformat()
                }
                for data in training_data
            ]
        })
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/model/train', methods=['POST'])
def train_model():
    """Trigger model training"""
    try:
        # This would typically be a long-running task
        # In production, you'd want to use a task queue like Celery
        return jsonify({
            'message': 'Model training initiated',
            'status': 'pending'
        })
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/model/status', methods=['GET'])
def get_model_status():
    """Get current model status"""
    try:
        # This would typically check the status of the training task
        return jsonify({
            'status': 'ready',
            'last_trained': None,
            'accuracy': None
        })
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
