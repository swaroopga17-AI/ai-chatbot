import requests
import os

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def query_hf(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    except Exception as e:
        return f"❌ Connection error: {e}"

    # If API failed
    if response.status_code != 200:
        return f"❌ API Error {response.status_code}: {response.text}"

    try:
        result = response.json()
    except:
        return "❌ Failed to read AI response."

    # If HuggingFace sends error message
    if isinstance(result, dict) and "error" in result:
        return f"⚠️ HuggingFace Error: {result['error']}"

    # If valid answer comes
    if isinstance(result, list) and len(result) > 0:
        if "generated_text" in result[0]:
            return result[0]["generated_text"]

    # Fallback
    return "⚠️ Unexpected response format from AI."
