


## File Structure

```
Folder PATH listing for volume Windows-SSD
Volume serial number is DECC-298C
C:
📂 Project Root  
├── .dockerignore          # Specifies files and directories to ignore when building a Docker image  
├── .gitignore             # Specifies files and directories to exclude from Git version control  
├── structure.txt          # Describes the file structure of the project  
├── README.md           # Documentation and setup instructions for the backend  

📂 client                   # Frontend client application  
│   ├── index.html         # Main HTML file for the client-side user interface  
│   ├── package.json       # Defines dependencies and scripts for the client application  
│   ├── pnpm-lock.yaml     # Lockfile for managing exact dependency versions with pnpm  
│   ├── script.js          # Client-side JavaScript logic  
│   └── 📂 node_modules    # Dependencies installed by pnpm (not included in version control)  

📂 server                   # Backend server application  
│   ├── Dockerfile          # Docker configuration for containerizing the server  
│   ├── main.py             # Entry point of the backend server application  
│   ├── requirements.txt    # Python dependencies for the server  

│   📂 model                # Machine learning model directory  
│   │   ├── train.py        # Script for training the machine learning model  
│   │   └── 📂 detect       # Directory for model detection results and configurations  
│   │       └── blackjack-model-final  
│   │           ├── args.yaml         # Configuration and parameters for the detection model  
│   │           ├── results.csv       # Results from the model's detection tests  
│   │           └── 📂 weights        # Directory containing the model weights  
│   │               ├── best.pt       # Best-performing model weights  
│   │               └── last.pt       # Weights from the most recent training  

│   📂 service              # Server services and logic  
│   │   └── vision.py       # Vision service for handling computer vision tasks  

│   📂 test                 # Folder containing the test scripts
│   │   └── vision.test.py  # Testing the core functions of the api
│   │   └── main.test.py    # Testing the http and websoction communications of fastapi 

│   📂 venv                 # Python virtual environment for managing dependencies (not included in version control)  


```