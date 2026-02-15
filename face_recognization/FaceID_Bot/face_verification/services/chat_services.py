from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["face_recognition_db"]
chats_collection = db["chats"]

def save_chat(user_id, user_message, bot_response):
    """Save a chat message to MongoDB"""
    chat_doc = {
        "user_id": user_id,
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.utcnow()
    }
    
    result = chats_collection.insert_one(chat_doc)
    return str(result.inserted_id)

def get_user_chats(user_id):
    """Retrieve all chats for a specific user"""
    chats = list(chats_collection.find(
        {"user_id": user_id},
        sort=[("timestamp", 1)]
    ))
    
    # Convert ObjectId to string for serialization
    for chat in chats:
        chat["_id"] = str(chat["_id"])
    
    return chats

def clear_user_chats(user_id):
    """Delete all chats for a specific user"""
    result = chats_collection.delete_many({"user_id": user_id})
    return result.deleted_count

