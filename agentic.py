import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    import requests
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        return response.text
    except Exception as e:
        return f"Could not get weather for {city}: {str(e)}"

@function_tool
def get_restaurant(city: str, cuisine: str) -> str:
    """Find restaurants in a city by cuisine type."""
    # placeholder — replace with real restaurant API
    return f"Top {cuisine} restaurant in {city}: La Bella Vista, 4.8 stars, 123 Main St."

@function_tool
def get_flights(from_city: str, to_city: str, date: str) -> str:
    """Find available flights between two cities on a given date."""
    # placeholder — replace with real flights API
    return f"Flight from {from_city} to {to_city} on {date}: R1200, departs 08:00, arrives 10:00."

# create the agent
travel_agent = Agent(
    name="TravelAssistant",
    instructions="""You are a helpful travel assistant, with a funny personality 
    Use the available tools to answer questions about weather, restaurants and flights.
    Always be friendly responses.""",
    tools=[get_weather, get_restaurant, get_flights]
)

def main():
    print("Travel Assistant — type 'bye' to exit")
    print(50 * "-")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Goodbye!")
            break

        result = Runner.run_sync(travel_agent, user_input)
        print(f"Assistant: {result.final_output}")
        print()

if __name__ == "__main__":
    main()