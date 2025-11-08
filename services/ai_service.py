import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

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
