from google import genai
from google.genai import types
import chromadb
import json
from pathlib import Path
from chromadb.utils import embedding_functions
from game_data_parser import get_today_game_data

# --- 1. Setup Gemini & DB ---
def load_gemini_config(path: Path) -> dict:
    cfg = {}
    try:
        if path.exists() and path.stat().st_size > 0:
            with path.open("r", encoding="utf-8") as f:
                cfg = json.load(f)
    except Exception as e:
        # If JSON is malformed or unreadable, raise so the server fails fast.
        raise RuntimeError(f"Failed to load Gemini config from {path}: {e}")

    api_key = cfg.get("api_key")
    model = cfg.get("model") or "gemini-3-flash-preview"

    return {"api_key": api_key, "model": model}

CONFIG_PATH = Path(__file__).resolve().parent / "gemini_api_config.json"
config = load_gemini_config(CONFIG_PATH)
print(f" ✈️  Load LLM model config: {config}")

client = genai.Client(api_key = config["api_key"])

db = chromadb.PersistentClient(path="./stardew_knowledge")
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = db.get_collection(name="stardew_wiki", embedding_function=embed_fn)

# --- 2. Fetch Context ---
def get_farm_status():
    farm_status = get_today_game_data()
    print(f" 🏡 Current Farm Status: {farm_status}")
    return farm_status

def search_wiki(query: str):
    """
    Searches the Stardew Valley Wiki for information about crops, 
    NPCs, festivals, and game mechanics.
    """
    # query = f"What to do in today's date with current farm status?"
    results = collection.query(query_texts=[query], n_results=3, include=['documents'])
    if results['documents']:
        context = "\n\n".join(results['documents'][0])
        return f"Wiki Results for '{query}':\n{context}"
    
    return "No relevant Wiki information found."

# --- 2. The Agent Logic ---
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


# --- 3. Execution ---
strategy = generate_daily_strategy()
print(f" 🌟 JUNIMO STRATEGY FOR TODAY\n")
print(strategy)