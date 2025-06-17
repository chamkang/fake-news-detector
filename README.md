{{ ... }}
# Fake News Image Detection Platform

A web-based platform that uses machine learning to detect fake images, built with React, Node.js, and Python.

## System Architecture

```
React (Client) -> Node.js + Express (API Server) -> Python (ML Service) -> CNN Model
```

## Project Structure

```
/fake_news_detector
├── /client             # React frontend
├── /server            # Node.js backend
├── /ml_service        # Python ML service
└── /data             # Datasets and sample images
```

## Features

- Image upload via file or URL
- Real-time image analysis
- Fake/Real prediction with confidence score
- Modern, responsive UI with TailwindCSS

## Tech Stack

### Frontend (client)
- React 18
- TailwindCSS
- Axios
- React Dropzone

### Backend (server)
- Node.js
- Express
- Multer (file upload)
- Axios

### ML Service
- Python 3.8+
- FastAPI
- PyTorch/TensorFlow
- OpenCV
- Pillow
- exifread

## Setup Instructions

### 1. Frontend Setup
```bash
cd client
npm install
npm start
```

### 2. Backend Setup
```bash
cd server
npm install
npm start
```

### 3. ML Service Setup
```bash
cd ml_service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Environment Variables

Create `.env` files in each directory:

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:3001
```

### Backend (.env)
```
PORT=3001
ML_SERVICE_URL=http://localhost:5000
```

### ML Service (.env)
```
PORT=5000
MODEL_PATH=./models/fake_detector.pt
```

## API Endpoints

### Backend API (Node.js)
- `POST /api/analyze` - Analyze image (file upload or URL)

### ML Service API (Python)
- `POST /predict` - Get prediction for image

## Development

1. Start the ML service:
```bash
cd ml_service
python main.py
```

2. Start the Node.js backend:
```bash
cd server
npm run dev
```

3. Start the React frontend:
```bash
cd client
npm start
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
{{ ... }}
