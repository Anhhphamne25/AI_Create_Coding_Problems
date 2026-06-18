# AI Create Coding Problems

An AI-powered system for automatically generating programming problems using Google Generative AI, with an automated critic workflow to ensure problem quality.

## 🎯 Features

- **Automatic problem generation**: Uses Google Generative AI (Gemini) to generate programming problems
- **Automated critic workflow**: AI reviews and approves generated problems
- **Improvement loop**: If a problem does not meet the quality requirements, the AI automatically revises it
- **RESTful API**: Provides an endpoint for generating programming problems
- **Multi-language support**: Supports generating problems for Python, Java, C++, and more
- **Difficulty evaluation**: Supports difficulty levels such as `easy`, `medium`, and `hard`

## 📋 Requirements

- Python 3.9+
- Google API Key for Generative AI
- pip package manager

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd AI_Create_Coding_Problems
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_API_MODEL=gemini-3-flash-preview
LOOP_COUNT=2
```

**Environment variables:**

- `GOOGLE_API_KEY`: Google Generative AI API key, required
- `GOOGLE_API_MODEL`: Gemini model to use, default: `gemini-3-flash-preview`
- `LOOP_COUNT`: Maximum number of generator-critic iterations, default: `1`

## 📦 Project Structure

```text
AI_Create_Coding_Problems/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   └── config.py           # Application settings
│   ├── modules/
│   │   ├── agents/
│   │   │   └── agent.py        # Generator and Critic agents
│   │   ├── prompts/
│   │   │   ├── generator_prompt.py
│   │   │   └── critic_prompt.py
│   │   ├── schemas/
│   │   │   └── schema.py       # Pydantic models
│   │   ├── services.py         # Business logic
│   │   └── workflow.py         # LangGraph workflow
│   └── routes/
│       └── create_problem.py   # API endpoints
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables, not committed
└── README.md                   # Documentation
```

## 🔧 API Reference

### Create a Programming Problem

**Endpoint:**

```http
POST /api/create_problem
```

**Request Body:**

```json
{
  "topic": "array",
  "difficulty": "easy",
  "language": "Python"
}
```

**Parameters:**

- `topic` string: The programming topic, for example: `array`, `tree`, `sorting`
- `difficulty` string: Problem difficulty: `easy`, `medium`, or `hard`. Default: `easy`
- `language` string: Programming language. Default: `Python`

**Response — Success 200:**

```json
{
  "title": "Calculate the Sum of an Array",
  "description": "Given an array of n integers, calculate the sum of all elements in the array.",
  "examples": [
    {
      "input": "5\n1 2 3 4 5",
      "output": "15"
    }
  ],
  "constraints": ["1 <= n <= 10^5", "-10^9 <= ai <= 10^9"],
  "note": ""
}
```

**Response — Error 500:**

```json
{
  "detail": "Error message"
}
```

### Health Check

**Endpoint:**

```http
GET /health
```

**Response:**

```json
{
  "status": "ok"
}
```

### Root

**Endpoint:**

```http
GET /
```

**Response:**

```json
{
  "message": "Welcome to the Create Problems by AI API!"
}
```

## 🤖 Workflow

```text
Request (/api/create_problem)
    ↓
[CreateProblemRequest parsing]
    ↓
[ProblemGenerationService.generate_problem()]
    ↓
[LangGraph Workflow Start]
    ├─→ [Generator Node]
    │   └─→ GeneratorAgent.run(topic, difficulty, language)
    │       └─→ LLM generates ProgrammingProblem
    │
    └─→ [Loop: up to LOOP_COUNT times]
        ├─→ [Critic Node]
        │   └─→ CriticAgent.run(problem)
        │       └─→ LLM returns CriticResponse
        │
        ├─→ [Check: is_approved?]
        │   ├─ YES → Return problem with status="approved"
        │   └─ NO → Continue to Generator for revision
        │
        └─→ [Generator Node - Revision]
            └─→ GeneratorAgent.run(refined_topic)
                └─→ LLM generates an improved ProgrammingProblem
    ↓
[Return final ProgrammingProblem]
```

## 🛠️ Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://localhost:8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📝 Usage Examples

### Using curl

```bash
curl -X POST "http://localhost:8000/api/create_problem" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "array",
    "difficulty": "medium",
    "language": "Python"
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/create_problem",
    json={
        "topic": "binary search",
        "difficulty": "hard",
        "language": "Java"
    }
)

problem = response.json()
print(f"Title: {problem['title']}")
print(f"Description: {problem['description']}")
print(f"Constraints: {problem['constraints']}")
```

## 🔑 Key Concepts

### GeneratorAgent

- Uses LangChain and Google Generative AI to generate programming problems
- Uses `temperature = 0.7` to balance creativity and control
- Returns a structured `ProgrammingProblem` object

### CriticAgent

- Reviews the generated programming problem
- Uses `temperature = 0` for deterministic evaluation
- Returns a `CriticResponse` containing approval status and feedback

### ProblemGenerationService

- Manages the generator-critic loop
- Limits the number of iterations based on `LOOP_COUNT`
- Marks the final problem status as `approved` or `draft`

### LangGraph Workflow

- Defines the problem-generation process using `StateGraph`
- Routes the flow based on the critic result, such as `is_approved`
- Supports automatic retry and revision using critic feedback

## 📊 Model Response Format

```python
class ProgrammingProblem:
    title: str                    # Problem title
    description: str              # Detailed problem description
    examples: List[Example]       # List of input/output examples
    constraints: List[str]        # List of constraints
    note: str                     # Additional notes
```

## 🐛 Troubleshooting

### `GOOGLE_API_KEY is not configured`

- Make sure the `.env` file exists and contains `GOOGLE_API_KEY`
- Or set the environment variable manually:

```bash
export GOOGLE_API_KEY=your-key
```

### Model `gemini-3-flash-preview` not found

- Check the valid model name in Google AI Studio
- Update `GOOGLE_API_MODEL` in the `.env` file

### High `LOOP_COUNT` causes slow responses

- Reduce `LOOP_COUNT` in the `.env` file
- Or increase the request timeout

## 📚 Tech Stack

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **LangChain**: LLM orchestration
- **LangGraph**: Workflow automation
- **Google Generative AI**: LLM provider
- **Uvicorn**: ASGI server

## 🤝 Contributing

Please open an issue or submit a pull request to improve this project.

## 📄 License

MIT License

---

**Author:** AI Development Team
**Version:** 1.0.0
