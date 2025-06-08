from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from fastapi.responses import HTMLResponse
import os
import numpy as np
from app.audio_utils import extract_mfcc
from app.voice_matcher import is_voice_match
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import random
import whisper
import difflib

import os
print("Current dir:", os.getcwd())
print("Static files:", os.listdir("Static"))

# Load Whisper only once
whisper_model = whisper.load_model("base")

app = FastAPI()

CHALLENGE_PHRASES = [
    "I solemnly swear that this is my real voice used for authentication",
    "Secure systems are those that ask for both something you know and something you are",
    "The quick brown fox jumps over the lazy dog and then runs through the forest",
    "Artificial intelligence is revolutionizing the way we think about identity verification",
    "Today is the perfect day to test our voice authentication challenge system properly"
    "I never imagined that a single decision could change the entire course of my life",
    "If you ever need someone to talk to, just remember that Im always here for you",
    "The sound of rain tapping against the window always makes me feel so peaceful inside",
    "Sometimes the best adventures begin when you step outside your comfort zone",
    "I’ve always wondered what it would be like to travel the world with no set destination",
    "Whenever I smell fresh bread baking, I’m instantly reminded of my childhood kitchen",
    "It’s amazing how a simple act of kindness can brighten someone’s entire day",
    "No matter how tough things get, I believe that everything happens for a reason",
    "Watching the sunrise from the top of the mountain was truly a breathtaking experience",
    "If we work together and support each other, there’s nothing we can’t accomplish."
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017/")
db = client.voice_auth
students = db.students

UPLOAD_DIR = "recordings"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/Static", StaticFiles(directory="Static"), name="Static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/enroll.html", encoding="utf-8") as f:
        return f.read()

@app.get("/verify-page", response_class=HTMLResponse)
async def verify_page():
    return open(os.path.join("static", "verify.html"), encoding="utf-8").read()

@app.get("/get-challenge")
async def get_challenge():
    phrase = random.choice(CHALLENGE_PHRASES)
    return JSONResponse(content={"challenge": phrase})

@app.post("/enroll")
async def enroll_student(name: str = Form(...), voice_sample: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, f"enroll_{voice_sample.filename}")
    with open(file_path, "wb") as f:
        f.write(await voice_sample.read())

    mfcc = extract_mfcc(file_path)
    students.update_one(
        {"name": name},
        {"$set": {"mfcc": mfcc.tolist()}},
        upsert=True
    )
    return {"message": f"{name} enrolled successfully"}

@app.post("/verify")
async def verify_student(
    name: str = Form(...),
    challenge_phrase: str = Form(...),
    voice_sample: UploadFile = File(...)
):
    file_path = os.path.join(UPLOAD_DIR, f"verify_{voice_sample.filename}")
    with open(file_path, "wb") as f:
        f.write(await voice_sample.read())

    student = students.find_one({"name": name})
    if not student:
        return {"verified": False, "message": "❌ Student not found."}

    stored_mfcc = np.array(student["mfcc"])
    voice_match = is_voice_match(file_path, stored_mfcc)

    whisper_model = whisper.load_model("base")
    result = whisper_model.transcribe(file_path)
    transcript = result["text"].strip().lower()


    from difflib import SequenceMatcher
    similarity = SequenceMatcher(None, transcript, challenge_phrase.lower()).ratio()

    print(f"Transcript: {transcript}")
    print(f"Expected: {challenge_phrase}")
    print(f"Similarity: {similarity:.2f}")

    if voice_match and similarity > 0.75:
        return {"verified": True, "message": "✅ Identity Verified!"}
    elif voice_match:
        return {"verified": False, "message": "⚠️ Voice matched, but phrase mismatch."}
    else:
        return {"verified": False, "message": "❌ Verification failed."}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
