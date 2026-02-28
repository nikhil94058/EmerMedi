This `SETUP.md` is designed for a backend developer to deploy and integrate the **Emergency Sound Detection System**.

---

# 🚨 Emergency Sound Detection System - Setup Guide

This project uses a **Convolutional Neural Network (CNN)** to detect emotions in audio and categorize them into emergency levels (Emergency, Non-Emergency, Neutral).

## 📁 Project Structure
```text
/project-root
│
├── /models
│   ├── server.py              # Flask AI API
│   └── Emotion_Voice_Detection_Model.h5  # Pre-trained CNN Model
│
├── /frontend (Next.js)
│   ├── /public
│   │   └── sound.wav          # Sample audio for testing
│   └── /app/api/analyze
│       └── route.js           # Next.js bridge to Flask
│
└── requirements.txt           # Python dependencies
```

---

## 🐍 1. Backend Setup (Python/Flask)

### Prerequisites
- **Python 3.9 - 3.11** (TensorFlow is sensitive to versions)
- **FFmpeg**: Required by `librosa` for audio processing.
  - *Windows:* `choco install ffmpeg` or download from ffmpeg.org.
  - *Mac:* `brew install ffmpeg`

### Installation
1. Navigate to the `models` folder:
   ```bash
   cd models
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install flask tensorflow librosa numpy h5py requests
   ```

### Running the Server
```bash
python server.py
```
- The server will start at `http://localhost:5000`.
- It will automatically suppress oneDNN floating-point logs.

---

## 🤖 2. AI Logic & Mapping
The backend categorizes the model's numerical output (0-7) into three human-readable states:

| Model Index | Emotion | Emergency Category |
| :--- | :--- | :--- |
| 4, 5, 7 | Angry, Fearful, Surprised | **EMERGENCY** |
| 2, 3, 6 | Happy, Sad, Disgust | **NON-EMERGENCY** |
| 0, 1 | Neutral, Calm | **NEUTRAL** |

---

## 🌐 3. API Documentation

### **Endpoint: Predict Sound**
`POST http://localhost:5000/predict`

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:** `file` (Binary .wav file)

**Response (JSON):**
```json
{
  "status": "success",
  "detected_emotion": "fearful",
  "emergency_category": "emergency",
  "class_index": 5
}
```

---

## 🚀 4. Next.js Integration (The Bridge)

To avoid **CORS** issues and handle file system access, the Next.js app uses a server-side route.

**Route Logic (`/api/analyze`):**
1. Fetches `public/sound.wav`.
2. Packages it into a `FormData` object.
3. Forwards it to the Flask server (`:5000`).
4. Returns a simplified status to the frontend.

**Example Response from Next.js API:**
```json
{ "status": "emergency" }
```

---

## 🛠 5. Troubleshooting

### `FileNotFoundError` (.h5 file)
The `server.py` uses dynamic path detection:
```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'Emotion_Voice_Detection_Model.h5')
```
**Fix:** Ensure the `.h5` file is in the **same folder** as `server.py`.

### `oneDNN` Warning logs
If you see messy numerical warnings in the terminal, the following environment variable is already included in `server.py` to fix it:
```python
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
```

### Audio Processing Errors
Ensure the input file is a valid `.wav` file. `librosa` will automatically resample all input to **16,000Hz** to match the model's training parameters.

---

## 🧪 6. Manual Testing (cURL)
To test the backend without the frontend:
```bash
curl -X POST -F "file=@sound.wav" http://localhost:5000/predict
```