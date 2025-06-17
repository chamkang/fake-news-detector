import express from 'express';
import cors from 'cors';
import multer from 'multer';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import FormData from 'form-data';
import fs from 'fs';
import axios from 'axios';

// Load environment variables
dotenv.config();

const app = express();
const port = process.env.PORT || 3001;
const mlServiceUrl = process.env.ML_SERVICE_URL || 'http://localhost:5000';

// Get current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configure multer for file upload
const upload = multer({
  dest: path.join(__dirname, '../uploads/'),
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB limit
  },
  fileFilter: (req, file, cb) => {
    // Accept images only
    if (!file.originalname.match(/\.(jpg|jpeg|png|gif)$/)) {
      return cb(new Error('Only image files are allowed!'), false);
    }
    cb(null, true);
  },
});

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({ status: 'ok', message: 'Fake News Image Detection API is running' });
});

app.post('/api/analyze', upload.single('image'), async (req, res) => {
  try {
    if (!req.file && !req.body.url) {
      return res.status(400).json({
        status: 'error',
        message: 'No image file or URL provided',
      });
    }

    const form = new FormData();

    if (req.file) {
      // If file was uploaded
      const imageStream = fs.createReadStream(req.file.path);
      form.append('file', imageStream);
    } else {
      // If URL was provided
      try {
        const response = await axios.get(req.body.url, {
          responseType: 'arraybuffer',
        });
        const buffer = Buffer.from(response.data);
        form.append('file', buffer, 'image.jpg');
      } catch (error) {
        return res.status(400).json({
          status: 'error',
          message: 'Failed to download image from URL',
        });
      }
    }

    // Send to ML service
    try {
      const mlResponse = await axios.post(`${mlServiceUrl}/predict`, form, {
        headers: form.getHeaders(),
        timeout: 30000 // 30 second timeout
      });

      // Clean up uploaded file
      if (req.file) {
        fs.unlinkSync(req.file.path);
      }

      res.json(mlResponse.data);
    } catch (mlError) {
      console.error('ML Service Error:', mlError);
      res.status(500).json({
        status: 'error',
        message: mlError.response?.data?.message || 'Failed to get prediction from ML service'
      });
    } finally {
      // Clean up uploaded file
      if (req.file) {
        fs.unlinkSync(req.file.path);
      }
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      status: 'error',
      message: error.message || 'Internal server error',
    });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
