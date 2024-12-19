# Augmented Reality Blackjack Card Counting System

## Overview
This documentation provides an overview of the system and detailed instructions for setting up, running, and testing both the client and server components of the augmented reality Blackjack card counting system. It also includes guidelines for configuring the application, troubleshooting common issues, and running unit tests to ensure proper functionality.

### System Overview
The system enables real-time Blackjack card counting using augmented reality (AR) glasses integrated with a computer vision model (YOLOv5). It consists of two main components:
- **Client (Web Interface):** Visualizes detected cards through AR.
- **Server (Backend):** Processes video frames to detect cards using WebSocket for low-latency, bidirectional communication.

### Technologies Used
#### Client-Side:
- **Vite** (^5.2.0): Build tool and development server
- **Vanilla JavaScript:** For client-side code
- **Node.js** (20.18.0): Required for running the frontend server

#### Server-Side:
- **Python** (3.12.5): Backend scripting
- **FastAPI:** Web framework for building the backend API
- **Uvicorn:** ASGI server to run the FastAPI application
- **Ultralytics YOLOv5:** Object detection model for card detection
- **OpenCV:** For image processing (e.g., base64 to OpenCV format)
- **Density Clustering** (^1.3.0): Clustering algorithm to organize detected objects

---

## Requirements
### Client-Side:
- **Node.js** 20.18.0 or later
- **Vite** 5.2.0 or later

### Server-Side:
- **Python** 3.12.5
- Required Python packages:
  ```bash
  pip install uvicorn[standard] ultralytics fastapi opencv-python
  ```

---

## Running the Server
### Steps:
1. Install Python dependencies:
   ```bash
   pip install uvicorn[standard] ultralytics fastapi opencv-python
   ```
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   The server will start at `http://localhost:8000/`, with WebSocket communication available at `ws://localhost:8000/ws`.

---

## Running the Client
### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/mihkuno/BLACKJACK.git
   cd BLACKJACK
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the client:
   ```bash
   npm run dev
   ```
   The client will be accessible at `http://localhost:3000/` and will connect to the server at `ws://localhost:8000/ws`.

---

## Troubleshooting
### Common Issues:
1. **WebSocket connection fails:**
   - Ensure the server is running and accessible at `ws://localhost:8000/ws`.
   - Check firewall and network settings.

2. **Video frame not captured:**
   - Ensure the camera is properly connected and accessible.
   - Verify browser permissions for camera access.

3. **Card detection issues:**
   - Ensure the camera feed is clear and cards are well-lit.
   - Retrain the YOLOv5 model for specific card types if necessary.

4. **Server crash or high latency:**
   - Monitor server logs for errors.
   - Ensure sufficient system resources for image processing.

---

## Testing
### Unit Testing for `service.vision.py` Functions
#### Functions to Test:
- `from_b64`: Converts a base64 image string to an OpenCV image.
- `to_b64`: Converts an OpenCV image to a base64 string.
- `detect`: Detects cards using YOLO in a base64 image.

#### How to Run:
1. Install testing dependencies:
   ```bash
   pip install pytest unittest
   ```
2. Run unit tests:
   ```bash
   python -m unittest visual.test.py
   ```

### Testing the FastAPI App (`main.py`)
#### Key Components to Test:
- HTTP endpoint: `/test`
- WebSocket endpoint: `/ws`

#### How to Run:
1. Install FastAPI testing dependencies:
   ```bash
   pip install pytest httpx pytest-asyncio
   ```
2. Run tests:
   ```bash
   pytest
   ```

---

## Repository
- GitHub: [BLACKJACK Repository](https://github.com/mihkuno/BLACKJACK)

### Videos:
- [Video 1](https://www.facebook.com/share/v/1Bwt2gxn2p/)
- [Video 2](https://www.facebook.com/share/v/1PYwSfpzag/)

---

## File Structure
```plaintext
Project Root  
├── .dockerignore          # Specifies files to ignore for Docker  
├── .gitignore             # Specifies files to exclude from Git  
├── structure.txt          # File structure description  
├── README.md              # Documentation and setup instructions  

📂 client                   # Frontend application  
│   ├── index.html         # Main HTML file  
│   ├── package.json       # Dependencies and scripts  
│   ├── pnpm-lock.yaml     # Dependency lockfile  
│   ├── script.js          # Client-side JavaScript  
│   └── 📂 node_modules    # Installed dependencies  

📂 server                   # Backend application  
│   ├── Dockerfile         # Docker configuration  
│   ├── main.py            # Backend entry point  
│   ├── requirements.txt   # Python dependencies  
│   
│   📂 model               # ML model directory  
│   │   ├── train.py       # Training script  
│   │   └── 📂 detect      # Detection results  
│   │       ├── args.yaml         # Detection parameters  
│   │       ├── results.csv       # Detection test results  
│   │       └── 📂 weights        # Model weights  
│   │           ├── best.pt       # Best weights  
│   │           └── last.pt       # Latest weights  
│   
│   📂 service             # Server services and logic  
│   │   └── vision.py      # Vision service  
│   
│   📂 test                # Test scripts  
│   │   ├── vision.test.py # Core function tests  
│   │   └── main.test.py   # FastAPI endpoint tests  
│   
│   📂 venv                # Virtual environment  
```

