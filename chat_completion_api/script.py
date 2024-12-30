import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are PlatziVision, you have to introduce yourself to the user.",
        },
        {
            "role": "user",
            "content": "Hello, how are you?"
        },
        {
            "role": "assistant",
            "content": "Hello! I'm PlatziVision, your virtual assistant. How can I assist you today?"
        },
        {
            "role": "user",
            "content": "What is Platzi?"
        }
    ],
    max_tokens=100,
    temperature=0.5
)

print(response.choices[0].message.content)


