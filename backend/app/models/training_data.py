"""Module for managing training data models in the database."""
from datetime import datetime
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create database engine
DB_PATH = Path(__file__).parent.parent.parent / 'data' / 'training.db'
os.makedirs(DB_PATH.parent, exist_ok=True)
engine = create_engine(f'sqlite:///{DB_PATH}')

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

class TrainingData(db.Model):
    """Model for storing training data information"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(10), nullable=False)  # 'real' or 'fake'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrainingData {self.filename}>'
