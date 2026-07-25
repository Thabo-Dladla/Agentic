from agents import Agent, Runner, function_tool,SQLiteSession,RunContextWrapper
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
from dataclasses import dataclass
import os
from os import getenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@dataclass
class UserContext:
    user_id: str
    is_premium: bool
    user_facts: dict

#=========================tools=========================
@function_tool
def get_advanced_analytics(ctx: RunContextWrapper[UserContext])-> str:
    if ctx.context.is_premium:
        return f"You are a premium user, advanced anayltics information was retrived and sent to your email"
    return "You are a non premium user, you connot retrive advanced analytics information"

@function_tool
def fact_saver(ctx: RunContextWrapper[UserContext], key: str, value: str)-> str:
    ctx.context.user_facts[key] = value
    return "facts have been extacted and saved in persistent storage"

def dynaimic_builder(ctx: RunContextWrapper[UserContext],agent)-> str:
    facts = ctx.context.user_facts
    return f"""You are a helpful assitant,
    you can retrieve advanced analytics information for premium users, use the get_advanced_analytics function
    Here are facts abouts this user
    {facts},
    use them normally in a conversation,
    use the fact_saver function to save new facts"""
    
#=================creating contexts=============================
u_context = UserContext(
    user_id= "123_abc",
    is_premium=True,
    user_facts = {}
)
u_context_2 = UserContext(
    user_id= "123_abc",
    is_premium=False,
    user_facts = {}
)
#============================creating session=============================================
async def helper_function(session):
    history = await session.get_items()
    if len(history)>20:
        prompt = []
        prompt.append({"role": "system", "content": f"""You are a helpful assistant,attached here is a conversation history, your task is to summarize the conversation
                        such you make it smaller and concise while keeping all essential information that another AI agent can use it to continue the conversation"""})
        #to_be_summarized = {"to_be_summarized": history[:-5]}
        prompt.append({"role": "system", "content": f"Here is the conversation to summarize: {history[:-10]}"})
        stay_verbatim = history[-10:] 
        await session.clear_session()
        #prompt  = "Please summarize this information such that another AI agent can use it to continue the conversation, make sure to include all relevant information"
        response = client.responses.create(
        model  = "gpt-4.1",
        input  = prompt,
        )
        summarized  = response.output_text
        print(f"Original conversation:\n{history[:-10]}\n\n")
        print(f"\n\nSummarized conversation:\n{summarized}\n\n")
        await session.add_items([
            {"role": "system", "content": f"Summary of earlier conversation: {summarized}"},
            *stay_verbatim
        ])
#======================Agent==============================
agent = Agent[UserContext](
    name = "Persistent Agent",
    instructions =dynaimic_builder,
    tools =[get_advanced_analytics,fact_saver],
)

session = SQLiteSession("user_1234_conversation")
#
result = Runner.run_sync(agent,"Hello, my name is Alice",session=session,context=u_context)
print(f"Bot: {result.final_output}")
#=========================================================================
result = Runner.run_sync(agent,"My favourite hobby is playing soccer",session=session,context=u_context)
print(f"Bot: {result.final_output}")
#========================================================================
result = Runner.run_sync(agent,"My favourite colour is blue",session=session,context=u_context)
print(f"Bot: {result.final_output}")
#=========================================================================
result = Runner.run_sync(agent,"My favourite food is pizza",session=session,context=u_context)
print(f"Bot: {result.final_output}")
#==========================================================================
print("\nFacts:", u_context.user_facts)
print("\n")
print("======================Main user loop(premium user)===========================")
turn =3
while turn>0:
    user_input = input("User: ")
    result = Runner.run_sync(agent,user_input,session=session,context=u_context)
    print(f"Bot: {result.final_output}")
    asyncio.run(helper_function(session))
    turn -=1
#==============Fact updater ====================================   
print("\n\nUpdated facts:", u_context.user_facts)
async def print_history(session):
    history = await session.get_items()
    for item in history:
        print(f"Conversation history:\n{item["content"]}")
#asyncio.run(print_history(session))
#asyncio.run(helper_function(session))
#========================================================================

#========================================================================
