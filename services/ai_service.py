import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

load_dotenv()

def get_openrouter_summary_stream(text: str, language: str = "en"):
    """Stream summary from OpenRouter with free models - yields text chunks"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY not found")

    prompt = f"""Create a detailed summary in {'English' if language == 'en' else 'German'}.

Structure:
🎯 TITLE: Create a descriptive title
📝 OVERVIEW: 2-3 sentences brief context
🔑 KEY POINTS: Main arguments with examples
💡 MAIN TAKEAWAYS: 3-5 practical insights
🔄 CONTEXT: Broader context discussion

Text to summarize:
{text}"""

    # Try multiple free models in order of preference
    free_models = [
        "google/gemma-2-9b-it:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "meta-llama/llama-3.2-1b-instruct:free"
    ]

    last_error = None
    for model_name in free_models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "stream": True
                },
                timeout=60,
                stream=True
            )

            if response.status_code == 200:
                # Stream the response
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            data_str = line_text[6:]
                            if data_str == '[DONE]':
                                return
                            try:
                                import json
                                data = json.loads(data_str)
                                if 'choices' in data and len(data['choices']) > 0:
                                    delta = data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        yield delta['content']
                            except:
                                continue
                return  # Successfully streamed

            last_error = f"Model {model_name}: {response.text}"
        except Exception as e:
            last_error = f"Model {model_name}: {str(e)}"
            continue

    # If all models fail, raise the last error
    raise Exception(f"All free models failed. Last error: {last_error}")

def get_openrouter_summary(text: str, language: str = "en", model: str = "google/gemma-2-9b-it:free") -> str:
    """Generate summary using OpenRouter with free models (non-streaming)"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY not found")

    prompt = f"""Create a detailed summary in {'English' if language == 'en' else 'German'}.

Structure:
🎯 TITLE: Create a descriptive title
📝 OVERVIEW: 2-3 sentences brief context
🔑 KEY POINTS: Main arguments with examples
💡 MAIN TAKEAWAYS: 3-5 practical insights
🔄 CONTEXT: Broader context discussion

Text to summarize:
{text}"""

    # Try multiple free models in order of preference
    free_models = [
        "google/gemma-2-9b-it:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "meta-llama/llama-3.2-1b-instruct:free"
    ]

    last_error = None
    for model_name in free_models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=60
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            last_error = f"Model {model_name}: {response.text}"
        except Exception as e:
            last_error = f"Model {model_name}: {str(e)}"
            continue

    # If all models fail, raise the last error
    raise Exception(f"All free models failed. Last error: {last_error}")

def get_gemini_summary(text: str, language: str = "en") -> str:
    """Generate summary using Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not found")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""Create a detailed summary in {'English' if language == 'en' else 'German'}.

Structure:
🎯 TITLE: Create a descriptive title
📝 OVERVIEW: 2-3 sentences brief context
🔑 KEY POINTS: Main arguments with examples
💡 MAIN TAKEAWAYS: 3-5 practical insights
🔄 CONTEXT: Broader context discussion

Text to summarize:
{text}"""

    response = model.generate_content(prompt)
    return response.text

def chunk_text(text: str, chunk_size: int = 7000, overlap: int = 1000) -> list:
    """Split text into overlapping chunks"""
    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1

        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            # Keep last 'overlap' characters for context
            overlap_words = []
            overlap_length = 0
            for w in reversed(current_chunk):
                if overlap_length >= overlap:
                    break
                overlap_words.insert(0, w)
                overlap_length += len(w) + 1
            current_chunk = overlap_words
            current_length = overlap_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_with_chunks(text: str, language: str = "en", ai_model: str = "openrouter") -> str:
    """Handle long transcripts with chunking"""
    chunks = chunk_text(text)

    # Select the appropriate AI function
    if ai_model == "openrouter":
        ai_function = get_openrouter_summary
    else:
        ai_function = get_gemini_summary

    if len(chunks) == 1:
        # Short video, direct summary
        return ai_function(text, language)

    # Process each chunk
    intermediate_summaries = []
    for i, chunk in enumerate(chunks):
        prompt = f"Create a detailed summary of section {i+1}. Maintain all important information.\n\nText: {chunk}"
        summary = ai_function(prompt, language)
        intermediate_summaries.append(summary)

    # Combine and create final summary
    combined = "\n\n=== Next Section ===\n\n".join(intermediate_summaries)
    final_summary = ai_function(combined, language)

    return final_summary
