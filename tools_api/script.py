import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# weather_tool

def get_weather(latitude: float, longitude: float) -> str:
    url_api = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url_api)
    weather_data = response.json()
    return json.dumps(weather_data) 

# Define the messages
messages=[
    {
        "role": "system",
        "content": "You are an assistant that can help with data about weather in real time using get_weather function.",
    },
    {
        "role": "user",
        "content": "What is the weather in Santiago, Chile?"
    }
]

functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather in a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "The latitude of the location"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "The longitude of the location"
                    }
                },
                "required": ["latitude", "longitude"]
            },
            "output": {
                "type": "string",
                "description": "The weather in the location requiered by the user"
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=functions
)

assistant_message = response.choices[0].message

print("Respuesta del asistente")
print(assistant_message)

if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        if tool_call.type == "function":
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "get_weather":
                print(f"calling get_weather function")
                weather_info = get_weather(
                    latitude=function_args.get("latitude"),
                    longitude=function_args.get("longitude")
                )

                messages.append(assistant_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": weather_info
                })

second_response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)

final_reply = second_response.choices[0].message.content
print(final_reply)






