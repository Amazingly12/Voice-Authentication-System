#  Voice Authentication System for Exam Monitoring

A secure voice authentication system built with FastAPI that uses **voice biometrics** and **challenge-response verification** to authenticate users. Users are enrolled by uploading voice samples, and verified by speaking randomly generated phrases checked for both speaker identity and phrase accuracy.

## Security Measures
Challenges restricts pre-recorded playback.
System verifies and nullifies AI voice assistants.
Whisper adds robustness to transcription across accents and noise.

##  Features

-  Voice-based user authentication
-  Live microphone recording via browser
-  Challenge phrase validation
-  Speech-to-text transcription using OpenAI Whisper
-  MongoDB database for storing user voiceprints
-  Clean HTML UI with a minimal dark theme
-  FastAPI (Python) 

##  Tech Stack

 Backend  --  FastAPI                  
 Audio  --  `librosa`, `pydub`       
 Transcription  --  OpenAI Whisper
 Database  --  MongoDB (via `pymongo`)  
 Frontend  --  HTML + CSS (vanilla JS)  

## Setup Instructions

Clone Project, In bash
```
git clone https://github.com/Amazingly12/Project-VA
cd Project-VA
python m venv .venv
.venv\Scripts\activate
``` 

Install required dependencies, In bash
```
pip install -r requirements.txt
```

Start MongoDB, In browser
```
mongo://localhost:27017
```

Finally run the server, In bash
```
uvicorn app.main:app --reload
```

## Enroll User
Provide a username and upload a '.wav' file
**On Windows To Upload a File** Record audio on **Sound Recorder** in a '.wav' format.

## Verify User
User requests a random phrase
browser records the user speaking 
Verifies using mfcc, Transcribes recording using Whisper and compares transcription to expected phrase.

If both criteria matches the user is verified!