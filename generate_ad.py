import os
import openai
from supabase import create_client

# Load ENV variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY[:6] + "...")

# Setup Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Setup OpenAI
openai.api_key = OPENAI_API_KEY

# Prompt and generate response
prompt = "Charming 3-bedroom home with a fully remodeled kitchen, fenced yard, and walkable to top-rated schools."
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
message = response['choices'][0]['message']['content']

# Log to Supabase
supabase.table("status_logs").insert({
    "agent_name": "RetailBoost-AI",
    "message": message,
    "timestamp": "now()"
}).execute()

print("✅ Log inserted:", message)

import time

while True:
    print("Idle... waiting for trigger")
    time.sleep(60)
