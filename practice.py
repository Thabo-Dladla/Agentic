from openai import OpenAI
import json
from datetime import datetime
import pytz
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

# Define a simple tool the agent can call
def get_weather(city: str) -> str:
    import requests
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        return response.text
    except Exception as e:
        return f"Could not get weather for {city}: {str(e)}"
    #return f"The weather in {city} is 22°C and sunny."

def get_time(timezone: str) -> str:
    tz = pytz.timezone(timezone)
    return datetime.now(tz).strftime("%H:%M:%S")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Name of the city"}
            },
            "required": ["city"]
        }
    }},
    {
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "Get the current time.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {"type": "string", "description": "timezone of the city"}
            },
            "required": ["timezone"]
        }
    } 
    }
    ]

# Step 1: Send the user message and tool definitions
messages = [{"role": "user", "content": "What's the weather and the time in Cape Town?"}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

# Step 2: Check if the model wants to call the tool
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    messages.append(response.choices[0].message)

    for tool in tool_calls:
        function_name = tool.function.name
        args = json.loads(tool.function.arguments)

        if function_name == "get_time":
            result = get_time(**args)
        elif function_name == "get_weather":
            result = get_weather(**args)

        messages.append({"role": "tool",
                         "tool_call_id": tool.id,
                         "content":result})
    
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    print(final_response.choices[0].message.content)