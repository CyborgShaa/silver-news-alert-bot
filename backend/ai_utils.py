# ai_utils.py

import os
import openai
import google.generativeai as genai
import logging

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Set API keys
openai.api_key = OPENAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Setup Gemini model
gemini_model = genai.GenerativeModel("gemini-pro")

# Optional: Configure logging
logging.basicConfig(level=logging.INFO)


def summarize_with_openai(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",  # You can change to gpt-4.1 if needed
            messages=[
                {"role": "system", "content": "You are a financial news summarizer. Keep it short, sharp, and market-relevant."},
                {"role": "user", "content": f"Summarize this silver-related news article in 2-3 lines:\n\n{text}"}
            ],
            max_tokens=150,
            temperature=0.3,
        )
        summary = response.choices[0].message.content.strip()
        logging.info("✅ OpenAI summary success.")
        return summary
    except Exception as e:
        logging.warning(f"⚠️ OpenAI failed: {e}")
        return None


def summarize_with_gemini(text: str) -> str:
    try:
        prompt = f"Summarize this silver-related financial article in 2-3 short sentences:\n\n{text}"
        response = gemini_model.generate_content(prompt)
        summary = response.text.strip()
        logging.info("✅ Gemini summary success.")
        return summary
    except Exception as e:
        logging.warning(f"⚠️ Gemini failed: {e}")
        return None


def fallback_summary(text: str) -> str:
    logging.warning("⚠️ Using fallback summary method.")
    return "Summary not available due to API failure. Please check the full article."


def get_best_summary(text: str) -> str:
    summary = summarize_with_openai(text)
    if summary:
        return summary

    summary = summarize_with_gemini(text)
    if summary:
        return summary

    return fallback_summary(text)
