"""Training script for fake news image detection model."""
import os
import argparse
from datetime import datetime

from model import ImageClassifier
from data_loader import get_data_loaders

def train_model(args):
    """Train the fake news detection model.
    
    Args:
        args: Command line arguments
    """
    # Create model directory if it doesn't exist
    os.makedirs(args.model_dir, exist_ok=True)
    
    # Generate model save path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(
        args.model_dir,
        f"fake_detector_{timestamp}.pt"
    )
    
    # Get data loaders
    train_loader, val_loader = get_data_loaders(
        args.data_dir,
        batch_size=args.batch_size,
        train_split=args.train_split
    )
    
    # Initialize and train model
    model = ImageClassifier()
    history = model.train(
        train_loader,
        val_loader=val_loader,
        epochs=args.epochs,
        save_path=model_path
    )
    
    print(f"\nTraining completed. Best model saved to: {model_path}")
    return history

def main():
    parser = argparse.ArgumentParser(description="Train fake news detection model")
    parser.add_argument(
        "--data_dir",
        type=str,
        required=True,
        help="Directory containing 'real' and 'fake' image subdirectories"
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default="./models",
        help="Directory to save trained models"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=32,
        help="Training batch size"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--train_split",
        type=float,
        default=0.8,
        help="Fraction of data to use for training"
    )
    
    args = parser.parse_args()
    train_model(args)

if __name__ == "__main__":
    main()
