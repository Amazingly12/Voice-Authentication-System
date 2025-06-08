from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["voice_auth"]
students = db["students"]
