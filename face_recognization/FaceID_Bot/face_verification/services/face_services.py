from pymongo import MongoClient
from deepface import DeepFace
import numpy as np

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["face_recognition_db"]
collection = db["users"]


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def register_face(image_path, user_id, name):
    embedding = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet",
        enforce_detection=True
    )[0]["embedding"]

    user_doc = {
        "user_id": user_id,
        "name": name,
        "embedding": embedding
    }

    collection.insert_one(user_doc)
    return True



def recognize_face(image_path, threshold=0.75):
    query_embedding = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet",
        enforce_detection=True
    )[0]["embedding"]

    best_match = None
    highest_similarity = -1

    for user in collection.find():
        similarity = cosine_similarity(query_embedding, user["embedding"])
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = user

    if best_match and highest_similarity >= threshold:
        return {
            "status": "recognized",
            "name": best_match["name"],
            "score": round(highest_similarity, 2)
        }

    return {
        "status": "unknown"
    }

