# chatbot.py
import google.generativeai as genai
import os

API_KEY = "AIzaSyDgUNaV4EJHZLASotuUcoaolPPXqVAdHNM"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def get_bot_reply(user_message):
    try:
        response = model.generate_content(user_message)
        return "🤖 " + response.text.strip()
    except Exception as e:
        return f"🤖 Error: {str(e)}"
