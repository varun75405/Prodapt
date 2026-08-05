# 🎓 AI Teacher's Assistant

## Overview
AI Teacher's Assistant is a full-stack web application designed to empower educators by automating the creation of high-quality educational materials. It leverages advanced AI to provide customized resources, saving teachers valuable time.

## Features
1. 📚 **Lesson Plan Generation**: Create comprehensive, structured lesson plans tailored by subject and grade level.
2. 📝 **Quiz Generation**: Automatically generate quizzes based on generated lesson plans.
3. 📄 **Learning Material Generation**: Create 6 different types of materials, including worksheets, flashcards, and homework.
4. 🔍 **Simplify Complex Topics**: Break down difficult concepts into 3 distinct levels (Elementary, Middle, High School).
5. 🎯 **Classroom Activity Generation**: Generate engaging activities across 6 different types (e.g., group work, games).

Plus: Login system, Privacy Policy, Rate limiting

## Architecture
```text
Frontend (Streamlit) -> Backend (FastAPI) -> Prompt Templates -> Groq API (Llama 3.3 70B)
```

## Tech Stack
| Component | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| AI Inference | Groq |
| Rate Limiting | slowapi |
| Validation | Pydantic |
| Environment | python-dotenv |

## Project Structure
```
ai-teachers-assistant/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── main.py
│   ├── requirements.txt
│   ├── pages/
│   │   ├── 1_📚_Lesson_Generator.py
│   │   └── ...
│   └── utils/
│       ├── api_client.py
│       ├── session.py
│       └── styles.py
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.9+
- Groq API key (free at console.groq.com)

### 1. Clone the repository
```bash
git clone <repo-url>
cd ai-teachers-assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 4. Install dependencies
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && pip install -r requirements.txt
```

### 5. Run the application
Terminal 1 (Backend):
```bash
cd backend
uvicorn main:app --reload --port 8000
```
Terminal 2 (Frontend):
```bash
cd frontend
streamlit run main.py --server.port 8501
```

### 6. Access
- Frontend: http://localhost:8501
- Backend API docs: http://localhost:8000/docs

## API Documentation
| Method | Path | Description | Rate Limit |
|---|---|---|---|
| POST | /login | Mock login | 10/min |
| POST | /generate-lesson | Generate lesson plan | 5/min |
| POST | /generate-quiz | Generate quiz | 5/min |
| POST | /generate-material | Generate learning material | 5/min |
| POST | /simplify-concept | Simplify a concept | 5/min |
| POST | /generate-activity | Generate classroom activity | 5/min |

## Environment Variables
| Variable | Description |
|---|---|
| GROQ_API_KEY | Required. API key for Groq |
| BACKEND_URL | Default http://localhost:8000 |
| BACKEND_HOST | Host for backend server |
| BACKEND_PORT | Port for backend server |

## Security
- API key hygiene: Keys are kept server-side only.
- Input validation: Prompts are length-restricted.
- Prompt injection guards: Structured templates limit abuse.
- Rate limiting: Prevents API spam.
- No PII: FERPA-friendly design avoiding student data.

## Models
- **Primary**: Llama 3.3 70B Versatile (via Groq)
- **Fallback**: Llama 3.1 8B Instant (via Groq)

## Future Enhancements
- Full authentication (JWT/OAuth)
- Database for saving generated content
- Content moderation layer
- Audit logging
- Export to PDF/DOCX
- Multi-language support
- Collaborative features

## License
MIT
