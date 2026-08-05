from enum import Enum

class GradeLevel(str, Enum):
    ELEMENTARY = "elementary"
    MIDDLE = "middle"
    HIGH = "high"

class Subject(str, Enum):
    MATH = "math"
    SCIENCE = "science"
    ENGLISH = "english"
    HISTORY = "history"
    ART = "art"
    GENERAL = "general"

class MaterialType(str, Enum):
    WORKSHEET = "worksheet"
    NOTES = "notes"
    FLASHCARDS = "flashcards"
    PRACTICE_EXERCISES = "practice_exercises"
    HOMEWORK = "homework"
    HANDOUTS = "handouts"

class ActivityType(str, Enum):
    GROUP_ACTIVITY = "group_activity"
    DISCUSSION = "discussion"
    ROLE_PLAY = "role_play"
    CLASSROOM_GAME = "classroom_game"
    ASSESSMENT = "assessment"
    EXIT_TICKET = "exit_ticket"

# Model constants
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

# Rate limiting
RATE_LIMIT = "5/minute"

# Input constraints
MAX_TOPIC_LENGTH = 200
MAX_CONCEPT_LENGTH = 200
MAX_LESSON_PLAN_LENGTH = 5000
MAX_USERNAME_LENGTH = 50
MIN_QUESTIONS = 1
MAX_QUESTIONS = 10
DEFAULT_QUESTIONS = 5

# API
API_TITLE = "AI Teacher's Assistant API"
API_DESCRIPTION = "An AI-powered assistant that helps educators create lesson plans, generate quizzes, prepare learning materials, simplify complex topics, and support classroom activities."
API_VERSION = "1.0.0"

# Groq
GROQ_TIMEOUT = 30  # seconds
GROQ_MAX_TOKENS = 4096
GROQ_TEMPERATURE = 0.7

MATERIAL_TYPE_DISPLAY = {
    MaterialType.WORKSHEET: "Worksheet",
    MaterialType.NOTES: "Study Notes",
    MaterialType.FLASHCARDS: "Flashcards",
    MaterialType.PRACTICE_EXERCISES: "Practice Exercises",
    MaterialType.HOMEWORK: "Homework Assignment",
    MaterialType.HANDOUTS: "Classroom Handout",
}

ACTIVITY_TYPE_DISPLAY = {
    ActivityType.GROUP_ACTIVITY: "Group Activity",
    ActivityType.DISCUSSION: "Discussion",
    ActivityType.ROLE_PLAY: "Role-Play",
    ActivityType.CLASSROOM_GAME: "Classroom Game",
    ActivityType.ASSESSMENT: "Assessment",
    ActivityType.EXIT_TICKET: "Exit Ticket",
}
