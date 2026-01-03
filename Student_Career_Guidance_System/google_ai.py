from google.ai.generativelanguage import GenerativeServiceClient
import os

client = GenerativeServiceClient(
    client_options={"api_key": os.getenv("GOOGLE_API_KEY", "")}
)

def generate_ai_insights(career, missing):
    prompt = f"Career: {career}. Missing skills: {', '.join(missing)}. Give 6-month roadmap."
    try:
        r = client.generate_content(
            model="models/gemini-pro",
            contents=[{"role":"user","parts":[{"text":prompt}]}]
        )
        return r.candidates[0].content.parts[0].text
    except:
        return "AI unavailable. Focus on learning missing skills with projects."
