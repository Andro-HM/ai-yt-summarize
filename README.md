# 🎥 YouTube Summarizer API

A lightweight FastAPI-based microservice that summarizes YouTube videos using **OpenRouter LLM models**.  
It fetches the video transcript, processes it, and returns a concise summary as a JSON response.

---

## 🚀 Features

- Summarize any YouTube video via a simple REST API  
- Automatically extracts the video ID from any valid YouTube URL  
- Fetches multilingual transcripts (English, Hindi, etc.)  
- Uses OpenRouter's free LLM models for summarization  
- Clean JSON responses (no streaming or frontend dependencies)  
- `.env` configuration for secure API keys  

---

## 🧩 Tech Stack

- **Python 3.10+**
- **FastAPI** — Web framework  
- **Uvicorn** — ASGI server  
- **OpenRouter API** — LLM summarization  
- **YouTube Transcript API** — Fetches video transcripts  
- **dotenv** — Environment variable management  

---

## 🗂️ Project Structure

```
ai-yt_summariser/
├── .env.example              # Example environment variables
├── .gitignore                # Excludes secrets, tests, and local files
├── main.py                   # FastAPI app entry point
├── api/
│   └── summarize.py          # POST /api/summarize route
├── services/
│   ├── ai_service.py         # Handles OpenRouter summarization
│   └── transcript_service.py # Fetches YouTube transcripts
└── utils/
    └── youtube.py            # Extracts YouTube video ID
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Andro-HM/ai-yt-summarize.git
cd ai-yt-summarize
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # on Windows
# or
source venv/bin/activate  # on macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root based on `.env.example`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

---

## ▶️ Running the Server

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:  
👉 **http://localhost:8000**

OpenAPI docs:  
👉 **http://localhost:8000/docs**

---

## 📡 API Usage

### Endpoint

```
POST /api/summarize
```

### Request Body

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "language": "en"
}
```

### Example (PowerShell / Windows)

```powershell
curl.exe -X POST "http://localhost:8000/api/summarize" `
  -H "Content-Type: application/json" `
  -d "{\"url\":\"https://youtu.be/fqyl5kbZ7Tw\",\"language\":\"en\"}"
```

### Example (Linux / macOS)

```bash
curl -X POST http://localhost:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/fqyl5kbZ7Tw", "language": "en"}'
```

### Response

```json
{
  "success": true,
  "summary": "This video discusses ...",
  "source": "youtube",
  "videoId": "fqyl5kbZ7Tw",
  "language": "en"
}
```

---

## 🧰 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | API key for OpenRouter LLMs | ✅ Yes |

---

## 🧠 How It Works

1. **Receive URL** → Extract YouTube video ID
2. **Fetch Transcript** → Retrieve text captions (auto language detection)
3. **Summarize** → Send transcript to OpenRouter model
4. **Return JSON** → Send clean summary response

---

## 🧾 Example Output

```json
{
  "success": true,
  "summary": "The video explains the core concept of ...",
  "source": "youtube",
  "videoId": "dQw4w9WgXcQ",
  "language": "en"
}
```

---

## 🛡️ Notes

- `.env` file is not included in the repo for security reasons.
- The `.env.example` file is provided as a template for setup.
- The repository intentionally excludes local frontend and test files.

---

## 🧑‍💻 Author

**Andro-HM**  
GitHub: [https://github.com/Andro-HM](https://github.com/Andro-HM)
