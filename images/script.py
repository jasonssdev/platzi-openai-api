import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
import base64

    # Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Define the messages
messages=[
    {
        "role": "system",
        "content": "You are an assistant that analyze images and return the description of the image.",
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Hi, can you describe this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpg;base64,{encode_image_to_base64("./images/image.jpg")}"
                }
            }
        ]
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages   
)

print(response.choices[0].message.content)