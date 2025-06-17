"""Image classification model for fake image detection."""
import os
from PIL import Image

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from dotenv import load_dotenv

class SimpleCNN(nn.Module):
    """Simple CNN architecture for fake image detection.
    
    Attributes:
        conv1 (nn.Conv2d): First convolutional layer.
        pool (nn.MaxPool2d): Max pooling layer.
        conv2 (nn.Conv2d): Second convolutional layer.
        fc1 (nn.Linear): First fully connected layer.
        fc2 (nn.Linear): Second fully connected layer.
        sigmoid (nn.Sigmoid): Sigmoid activation function.
    """
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 54 * 54, 64)
        self.fc2 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """Forward pass of the CNN.
        
        Args:
            x: Input tensor of shape (batch_size, 3, 224, 224)
            
        Returns:
            Tensor of shape (batch_size, 1) with values between 0 and 1
        """
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 54 * 54)
        x = torch.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

class ImageClassifier:
    """Image classifier for fake image detection."""
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SimpleCNN().to(self.device)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Load model if exists
        model_path = os.getenv("MODEL_PATH", "./models/fake_detector.pt")
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def predict(self, image: Image.Image) -> str:
        """Predict if an image is fake or real.
        
        Args:
            image: PIL Image to classify
            
        Returns:
            str: prediction label ('Fake' or 'Real')
        """
        # Transform image
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Get prediction
        with torch.no_grad():
            output = self.model(img_tensor)
            confidence = float(output[0][0])
            
        # Convert to label
        prediction = "Fake" if confidence > 0.5 else "Real"
        
        return prediction

    def train(self, train_loader, val_loader=None, epochs=10, save_path=None):
        """Train the model on new data.
        
        Args:
            train_loader: DataLoader with training data
            val_loader: Optional validation data loader
            epochs: Number of training epochs
            save_path: Optional path to save the best model
            
        Returns:
            dict: Training history with losses and accuracies
        """
        criterion = nn.BCELoss()
        optimizer = torch.optim.Adam(self.model.parameters())
        
        best_val_loss = float('inf')
        history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': []
        }
        
        for epoch in range(epochs):
            # Training phase
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            
            for inputs, labels in train_loader:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                predictions = (outputs > 0.5).float()
                train_correct += (predictions == labels).sum().item()
                train_total += labels.size(0)
            
            avg_train_loss = train_loss / len(train_loader)
            train_accuracy = train_correct / train_total
            
            history['train_loss'].append(avg_train_loss)
            history['train_acc'].append(train_accuracy)
            
            # Validation phase
            if val_loader:
                val_loss, val_accuracy = self._validate(val_loader, criterion)
                history['val_loss'].append(val_loss)
                history['val_acc'].append(val_accuracy)
                
                print(f'Epoch {epoch+1}/{epochs}:')
                print(f'  Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.4f}')
                print(f'  Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}')
                
                # Save best model
                if save_path and val_loss < best_val_loss:
                    best_val_loss = val_loss
                    torch.save(self.model.state_dict(), save_path)
            else:
                print(f'Epoch {epoch+1}/{epochs}:')
                print(f'  Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.4f}')
        
        return history
    
    def _validate(self, val_loader, criterion):
        """Run validation on the model.
        
        Args:
            val_loader: Validation data loader
            criterion: Loss function
            
        Returns:
            tuple: (validation loss, validation accuracy)
        """
        self.model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                predictions = (outputs > 0.5).float()
                val_correct += (predictions == labels).sum().item()
                val_total += labels.size(0)
        
        return val_loss / len(val_loader), val_correct / val_total
        
        self.model.eval()
        
        # Save model
        model_path = os.getenv("MODEL_PATH", "./models/fake_detector.pt")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        torch.save(self.model.state_dict(), model_path)
