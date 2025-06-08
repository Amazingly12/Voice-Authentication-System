import numpy as np
from pymongo import MongoClient
from app.audio_utils import extract_mfcc

client = MongoClient("mongodb://localhost:27017")
db = client["voice_auth"]
students = db["students"]

# Path to a known student's .wav file
path = "recordings/john.wav"
mfcc = extract_mfcc(path)

# Save to MongoDB
students.insert_one({
    "name": "John",
    "mfcc": mfcc.tolist()  # convert numpy array to list for JSON
})
