from google import genai
from google.genai import types
import chromadb
from my_package.utils.load_env_config import load_gemini_config
from chromadb.utils import embedding_functions
from my_package.utils.game_data_parser import get_today_game_data


db = chromadb.PersistentClient(path="./stardew_knowledge")
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = db.get_collection(name="stardew_wiki", embedding_function=embed_fn)

# can not use utils.tool_functions which are for agent
def get_farm_status():
    farm_status = get_today_game_data()
    print(f" 🏡 Current Farm Status: {farm_status}")
    return farm_status

def search_wiki(query: str):
    """
    Searches the Stardew Valley Wiki for information about crops, 
    NPCs, festivals, and game mechanics.
    """
    results = collection.query(query_texts=[query], n_results=3, include=['documents'])
    if results['documents']:
        context = "\n\n".join(results['documents'][0])
        return f"Wiki Results for '{query}':\n{context}"
    
    return "No relevant Wiki information found."


SYSTEM_PROMPT = """
You are JunimoMind, a high-level Stardew Valley strategist. 
Your goal is to help the player optimize their farm while maintaining a helpful, Junimo-like tone.
You operate in a loop of Thought, Action, Observation, and Answer.

1. THOUGHT: Describe what you are thinking and what you need to find out.
2. ACTION: Call a tool (get_farm_status or search_wiki) to get information.
3. OBSERVATION: Analyze the data returned by the tool.
4. ANSWER: Once you have all the information, provide the final response to the player.

Example:
Thought: I need to know the date to see if there is a birthday today.
Action: get_farm_status()
Observation: It is Spring 4.
Thought: Now I need to check who has a birthday on Spring 4.
Action: search_wiki("Spring 4 birthdays")
...and so on.

RULES:
1. ALWAYS call 'get_farm_status' first to see the current money, date, daily luck and weather.
2. ALWAYS search the Wiki (ChromaDB) for specific crop or fish data before giving numbers.
3. Be concise. Provide a 'Morning Greeting' followed by exactly 3 'Daily Tasks'.
4. If the player has low energy or low money, suggest foraging or socializing.
"""

config = load_gemini_config()

client = genai.Client(api_key = config["api_key"])

def generate_daily_strategy():
    tools=[get_farm_status, search_wiki]
    
    response = client.models.generate_content(
        model=config["model"],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=1.0,
            tools=tools,
        ),
        contents=f"nWhat should I do today?"
    )   

    # Print the agent's internal reasoning steps 
    """
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text') and part.text:
            print(f"🧠 THOUGHT: {part.text}")
        if part.function_call:
            print(f"🛠️ ACTION: {part.function_call.name}({part.function_call.args})")
    """
        
    return response.text


strategy = generate_daily_strategy()
print(f" 🌟 JUNIMO STRATEGY FOR TODAY\n")
print(strategy)