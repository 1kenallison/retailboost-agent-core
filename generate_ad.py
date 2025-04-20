import os
import openai
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:8]}")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_ad(property_description):
    prompt = f"Write a Facebook/Instagram-style real estate ad for this property:\n\n{property_description}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a real estate ad writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=250
    )

    ad_text = response.choices[0].message.content.strip()
print("Attempting Supabase insert...")

    supabase.table("status_logs").insert({
        "agent_name": "RetailBoost-AI",
        "message": f"Generated ad for: {property_description[:50]}...",
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
print("Insert successful.")


    return ad_text
