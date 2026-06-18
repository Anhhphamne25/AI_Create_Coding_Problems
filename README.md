# AI Create Coding Problems

Một hệ thống tạo đề bài lập trình tự động sử dụng AI (Google Generative AI), với quy trình phản biện tự động để đảm bảo chất lượng đề bài.

## 🎯 Tính năng

- **Tạo đề bài tự động**: Sử dụng Google Generative AI (Gemini) để sinh ra đề bài lập trình
- **Quy trình phản biện**: AI tự động kiểm tra và phê duyệt đề bài
- **Vòng lặp cải tiến**: Nếu đề bài chưa đạt yêu cầu, AI sẽ tự động chỉnh sửa
- **API RESTful**: Cung cấp endpoint để tạo đề bài
- **Hỗ trợ nhiều ngôn ngữ**: Có thể tạo đề bài cho Python, Java, C++, v.v.

## 📋 Yêu cầu

- Python 3.9+
- Google API Key (Generative AI)
- pip package manager

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd AI_Create_Coding_Problems
```

### 2. Tạo virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc:

```env
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_API_MODEL=gemini-3-flash-preview
LOOP_COUNT=2
```

**Các biến:**

- `GOOGLE_API_KEY`: Google Generative AI API key (bắt buộc)
- `GOOGLE_API_MODEL`: Model Gemini sử dụng (mặc định: gemini-3-flash-preview)
- `LOOP_COUNT`: Số lần tối đa vòng lặp generator-critic (mặc định: 1)

## 📦 Cấu trúc dự án

```
AI_Create_Coding_Problems/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   └── config.py          # Cấu hình settings
│   ├── modules/
│   │   ├── agents/
│   │   │   └── agent.py       # Generator & Critic agents
│   │   ├── prompts/
│   │   │   ├── generator_prompt.py
│   │   │   └── critic_prompt.py
│   │   ├── schemas/
│   │   │   └── schema.py      # Pydantic models
│   │   ├── services.py        # Business logic
│   │   └── workflow.py        # LangGraph workflow
│   └── routes/
│       └── create_problem.py  # API endpoints
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (chưa commit)
└── README.md                  # Documentation
```

## 🔧 API Reference

### Tạo đề bài

**Endpoint:**

```
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

- `topic` (string): Chủ đề bài tập (vd: "array", "tree", "sorting")
- `difficulty` (string): Độ khó - `easy`, `medium`, `hard` (mặc định: `easy`)
- `language` (string): Ngôn ngữ lập trình (mặc định: `Python`)

**Response (Success - 200):**

```json
{
  "title": "Tính tổng mảng",
  "description": "Cho một mảng gồm n số nguyên. Hãy tính tổng các phần tử trong mảng.",
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

**Response (Error - 500):**

```json
{
  "detail": "Error message"
}
```

### Health Check

**Endpoint:**

```
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

```
GET /
```

**Response:**

```json
{
  "message": "Welcome to the Create Problems by AI API!"
}
```

## 🤖 Luồng xử lý

```
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
    └─→ [Loop: max LOOP_COUNT times]
        ├─→ [Critic Node]
        │   └─→ CriticAgent.run(problem)
        │       └─→ LLM returns CriticResponse
        │
        ├─→ [Check: is_approved?]
        │   ├─ YES → Return problem with status="approved"
        │   └─ NO → Continue to Generator (revise)
        │
        └─→ [Generator Node - Revise]
            └─→ GeneratorAgent.run(refined_topic)
                └─→ LLM generates improved ProgrammingProblem
    ↓
[Return final ProgrammingProblem]
```

## 🛠️ Chạy ứng dụng

### Development mode

```bash
uvicorn app.main:app --reload
```

Ứng dụng sẽ chạy tại: `http://localhost:8000`

### Production mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📝 Ví dụ sử dụng

### Sử dụng curl

```bash
curl -X POST "http://localhost:8000/api/create_problem" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "array",
    "difficulty": "medium",
    "language": "Python"
  }'
```

### Sử dụng Python

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

## 🔑 Các khái niệm chính

### GeneratorAgent

- Sử dụng LangChain + Google Generative AI để sinh ra đề bài
- Temperature = 0.7 (creative nhưng controlled)
- Trả về object `ProgrammingProblem` đã structured

### CriticAgent

- Đánh giá đề bài đã sinh ra
- Temperature = 0 (deterministic)
- Trả về `CriticResponse` với trạng thái approved và feedback

### ProblemGenerationService

- Quản lý vòng lặp generator-critic
- Giới hạn số vòng theo `LOOP_COUNT`
- Đánh dấu status `approved` hoặc `draft`

### LangGraph Workflow

- Định nghĩa quy trình thông qua StateGraph
- Điều hướng dựa trên kết quả critic (`is_approved`)
- Hỗ trợ tự động retry với feedback

## 📊 Model Response Format

```python
class ProgrammingProblem:
    title: str                    # Tên đề bài
    description: str              # Mô tả chi tiết
    examples: List[Example]       # Danh sách ví dụ input/output
    constraints: List[str]        # Danh sách ràng buộc
    note: str                     # Ghi chú bổ sung
```

## 🐛 Troubleshooting

### "GOOGLE_API_KEY is not configured"

- Đảm bảo file `.env` tồn tại và có `GOOGLE_API_KEY`
- Hoặc set environment variable: `export GOOGLE_API_KEY=your-key`

### Model "gemini-3-flash-preview" not found

- Kiểm tra tên model hợp lệ từ Google AI Studio
- Cập nhật `GOOGLE_API_MODEL` trong `.env`

### LOOP_COUNT quá cao → chậm

- Giảm `LOOP_COUNT` trong `.env`
- Hoặc tăng thời gian timeout của request

## 📚 Công nghệ sử dụng

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **LangChain**: LLM orchestration
- **LangGraph**: Workflow automation
- **Google Generative AI**: LLM provider
- **Uvicorn**: ASGI server

## 🤝 Đóng góp

Vui lòng tạo issue hoặc pull request để cải thiện dự án.

## 📄 Giấy phép

MIT License

---

**Tác giả:** AI Development Team
**Phiên bản:** 1.0.0
