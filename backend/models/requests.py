from pydantic import BaseModel, Field
from backend.constants import GradeLevel, Subject, MaterialType, ActivityType

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Username for demo login")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "teacher123"
            }
        }
    }

class LessonRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200, description="Topic for the lesson plan")
    grade_level: GradeLevel = Field(..., description="Target grade level")
    subject: Subject = Field(..., description="Subject area")

    model_config = {
        "json_schema_extra": {
            "example": {
                "topic": "Photosynthesis",
                "grade_level": "middle",
                "subject": "science"
            }
        }
    }

class QuizRequest(BaseModel):
    lesson_plan: str = Field(..., min_length=1, max_length=5000, description="Lesson plan text to generate quiz from")
    num_questions: int = Field(default=5, ge=1, le=10, description="Number of quiz questions")

    model_config = {
        "json_schema_extra": {
            "example": {
                "lesson_plan": "A lesson plan about...",
                "num_questions": 5
            }
        }
    }

class MaterialRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    grade_level: GradeLevel
    subject: Subject
    material_type: MaterialType = Field(..., description="Type of learning material to generate")

    model_config = {
        "json_schema_extra": {
            "example": {
                "topic": "Fractions",
                "grade_level": "elementary",
                "subject": "math",
                "material_type": "worksheet"
            }
        }
    }

class SimplifyRequest(BaseModel):
    concept: str = Field(..., min_length=1, max_length=200, description="Complex concept to simplify")
    subject: Subject

    model_config = {
        "json_schema_extra": {
            "example": {
                "concept": "Quantum Mechanics",
                "subject": "science"
            }
        }
    }

class ActivityRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    grade_level: GradeLevel
    subject: Subject
    activity_type: ActivityType = Field(..., description="Type of classroom activity to generate")

    model_config = {
        "json_schema_extra": {
            "example": {
                "topic": "The Solar System",
                "grade_level": "middle",
                "subject": "science",
                "activity_type": "group_activity"
            }
        }
    }
