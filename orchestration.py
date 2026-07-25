from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
load_dotenv()
#-----tools-------------------------------------------
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny and warm."


@function_tool
def get_flights(from_city:str, to_city:str) -> str:
    return f"There is a flight from {from_city} to {to_city} on the 22nd of August 2026 at 20h00.\nThe flight number is 1234 and the airline is Air Travel."


#-----Agents-------------------------------------------
weather_agent  = Agent(
    name = "Weather Agent",
    instructions = ("Help users to check the current weather of given cities. Use the get_weather function."),
    tools = [get_weather],
)

flight_agent = Agent(
    name = "Flight Agent",
    instructions= ("Help find users flights from the given depature city to the destination city."
    "Use the get_flights function"),
    tools= [get_flights],
)
travel_agent = Agent(
    name = "TravelAgent",
    instructions = ("You are a Travel Assistant,"
    "You can help users find flights and check the weather of certain cities. "
    "You can use the get_weather and get_flights functions to help users with their queries."),
    #handoffs= [flight_agent,weather_agent]
    tools= [get_weather,get_flights]
)

#-----Main Loop-------------------------------------------

print(50*"*")
print("Hi please query about the weather of certain areas")
print(50*"*")
print(*"\n\n")
while True:
    user_input = input("User: ")
    if user_input in ["bye","exit"]:
        break
    result  = Runner.run_sync(travel_agent,user_input,max_turns = 5)
    answer = result.final_output
    print(f"Bot: {answer}")
    break