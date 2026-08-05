import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
REQUEST_TIMEOUT = 60

def _handle_request(func, *args, **kwargs):
    try:
        response = func(*args, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Failed to connect to the backend server. Please try again later.", "data": None, "model_used": None}
    except requests.exceptions.Timeout:
        return {"success": False, "message": "The request timed out. Please try again.", "data": None, "model_used": None}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {str(e)}", "data": None, "model_used": None}

def login(username: str) -> dict:
    return _handle_request(requests.post, f"{BACKEND_URL}/login", json={"username": username}, timeout=REQUEST_TIMEOUT)

def generate_lesson(topic: str, grade_level: str, subject: str) -> dict:
    return _handle_request(requests.post, f"{BACKEND_URL}/generate-lesson", json={"topic": topic, "grade_level": grade_level, "subject": subject}, timeout=REQUEST_TIMEOUT)

def generate_quiz(lesson_plan: str, num_questions: int = 5) -> dict:
    return _handle_request(requests.post, f"{BACKEND_URL}/generate-quiz", json={"lesson_plan": lesson_plan, "num_questions": num_questions}, timeout=REQUEST_TIMEOUT)

def generate_material(topic: str, grade_level: str, subject: str, material_type: str) -> dict:
    return _handle_request(requests.post, f"{BACKEND_URL}/generate-material", json={"topic": topic, "grade_level": grade_level, "subject": subject, "material_type": material_type}, timeout=REQUEST_TIMEOUT)

def simplify_concept(concept: str, subject: str) -> dict:
    return _handle_request(requests.post, f"{BACKEND_URL}/simplify-concept", json={"concept": concept, "subject": subject}, timeout=REQUEST_TIMEOUT)

def generate_activity(topic: str, grade_level: str, subject: str, activity_type: str) -> dict:
    return _handle_request(requests.post, f"{BACKEND_URL}/generate-activity", json={"topic": topic, "grade_level": grade_level, "subject": subject, "activity_type": activity_type}, timeout=REQUEST_TIMEOUT)
