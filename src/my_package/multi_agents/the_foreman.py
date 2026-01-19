from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from my_package.utils.load_gemini_config import load_gemini_config
from my_package.utils.tool_functions import get_farm_status, search_wiki, handle_tool_errors
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel
from rich.console import Console
from rich.markdown import Markdown

checkpointer = InMemorySaver()


print(f"-- Loading AI model config and game data")
config = load_gemini_config()

model = ChatGoogleGenerativeAI(
    model=config["model"],
    api_key=config["api_key"],
    temperature=1.0,
    max_tokens = 10000,
    timeout = 120000,
    max_retries=2,
)

tools = [get_farm_status, search_wiki]
middleware = [handle_tool_errors]

# -- Define the Specialists --
money_maker_agent = create_agent(
    model=model, 
    tools=tools,
    middleware=middleware,
    system_prompt="You are the money maker. Optimize for money. Focus on crops and animals. Maximize profit per tile; ensure crops don't die on season change.",
)

@tool("money_maker_agent", description="Agent optimize for monetization through crops and animals")  
def call_money_maker(query: str):  
    result = money_maker_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

socialite_agent = create_agent(
    model=model, 
    tools=tools,
    middleware=middleware,
    system_prompt="You are the Socialite. Focus on NPC hearts, birthdays, and festivals.",
)

@tool("socialite_agent", description="Agent focus on NPC, birthdays and festivals")  
def call_socialite(query: str):  
    result = socialite_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

scavenger_agent = create_agent(
    model=model, 
    tools=tools,
    middleware=middleware,
    system_prompt="You are the Scavenger. Focus on Community Center Bundles and active quests items.",
)

@tool("scavenger_agent", description="Agent focus on complete quests and building Community Center.")  
def call_scavenger(query: str):  
    result = scavenger_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content



# -- Build the Supervisor --
SYSTEM_PROMPT = """You are JunimoMind, a high-level Stardew Valley strategist. 
Your goal is to help the player optimize their farm while maintaining a helpful, Junimo-like tone.
You operate in a loop of Thought, Action, Observation, and Answer.

RULES:
1. ALWAYS call 'get_farm_status' first to see the current money, date, daily luck and weather.
2. ALWAYS search the Wiki (ChromaDB) for specific crop or fish data before giving numbers.
3. Be concise. Provide a 'Morning Greeting' followed by exactly 3 'Daily Tasks'.
4. If the player has low energy or low money, suggest foraging or socializing.

Example:
Thought: I need to know the date to see if there is a birthday today.
Action: get_farm_status()
Observation: It is Spring 4.
Thought: Now I need to check who has a birthday on Spring 4.
Action: search_wiki("Spring 4 birthdays")
...and so on.

You orchestrate a team of three specialists.
    1. Money maker (Money/Crops/Animals)
    2. Socialite (Friendship/Festivals)
    3. Scavenger (Quests/Bundles)

CRITICAL: When calling a tool, you must output ONLY the JSON arguments. Do not write Python code, do not add explanations, and do not use markdown code blocks inside the function call parameters. Use the exact tool name provided.
"""

print(f"-- Start reasoning")

class ResponseText(BaseModel):
    greetings: str
    todos: str

foreman_agent = create_agent(
    model=model,
    tools=[call_money_maker, call_socialite, call_scavenger],
    system_prompt=SYSTEM_PROMPT,
    response_format=ToolStrategy(ResponseText)
)

response = foreman_agent.invoke(
    {"messages": [{"role": "user", "content": "what should I do today?"}]},
)


print(f"-- Agent Response")

print(f" 🌟 JUNIMO STRATEGY FOR TODAY\n")
text = response['structured_response']
print(f" 👾 {text.greetings}\n")
console = Console()
md = Markdown(text.todos)
console.print(md)

