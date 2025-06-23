#!/usr/bin/env python3
from dotenv import load_dotenv 
import os  
import openai

load_dotenv(override=True) 
 
openai.api_key = os.getenv('OPENAI_API_KEY')  
client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "Test input, please say good if you understand this input."}
    ]
)

print(response.choices[0].message.content)