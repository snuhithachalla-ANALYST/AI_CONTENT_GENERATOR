from fastapi import FastAPI, HTTPException
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
api_key = os.getenv("GROQ_API_KEY")

client = None
if api_key:
    client = Groq(api_key=api_key)


@app.post("/generate")
def generate_content(
    topic: str,
    technology: str,
    content_type: str,
    tone: str
):
    prompt = f"""
Generate a {content_type}

Topic: {topic}
Technology: {technology}
Tone: {tone}
"""

    if client is None:
        return {
            "content": (
                f"Demo content for a {content_type} about {topic} in a {tone} tone "
                f"for {technology}. Replace GROQ_API_KEY in .env with a valid key to use real AI generation."
            )
        }

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "content": response.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))