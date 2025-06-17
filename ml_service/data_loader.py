"""Data loading and preprocessing utilities for fake news image detection."""
import os
from typing import Tuple

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

class FakeNewsDataset(Dataset):
    """Dataset for fake news image detection.
    
    Args:
        root_dir: Root directory containing 'real' and 'fake' subdirectories
        transform: Optional transform to be applied on images
    """
    def __init__(self, root_dir: str, transform=None):
        self.root_dir = root_dir
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Load all image paths and labels
        self.data = []
        
        # Load real images (label 0)
        real_dir = os.path.join(root_dir, 'real')
        if os.path.exists(real_dir):
            for img_name in os.listdir(real_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.data.append((
                        os.path.join(real_dir, img_name),
                        0  # Real label
                    ))
        
        # Load fake images (label 1)
        fake_dir = os.path.join(root_dir, 'fake')
        if os.path.exists(fake_dir):
            for img_name in os.listdir(fake_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.data.append((
                        os.path.join(fake_dir, img_name),
                        1  # Fake label
                    ))
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        img_path, label = self.data[idx]
        
        # Load and transform image
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        
        return image, torch.tensor([label], dtype=torch.float32)

def get_data_loaders(data_dir: str, batch_size: int = 32, train_split: float = 0.8):
    """Create training and validation data loaders.
    
    Args:
        data_dir: Directory containing 'real' and 'fake' subdirectories
        batch_size: Batch size for data loaders
        train_split: Fraction of data to use for training
        
    Returns:
        tuple: (train_loader, val_loader)
    """
    # Create dataset
    dataset = FakeNewsDataset(data_dir)
    
    # Split into train and validation
    train_size = int(train_split * len(dataset))
    val_size = len(dataset) - train_size
    
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        pin_memory=True
    )
    
    return train_loader, val_loader
