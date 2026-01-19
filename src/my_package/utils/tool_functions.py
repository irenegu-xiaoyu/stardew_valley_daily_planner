import chromadb
from chromadb.utils import embedding_functions
from my_package.utils.game_data_parser import get_today_game_data
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

db = chromadb.PersistentClient(path="./stardew_knowledge")
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = db.get_collection(name="stardew_wiki", embedding_function=embed_fn)

@tool
def get_farm_status():
    """Get farm status of today"""
    farm_status = get_today_game_data()
    print(f"  🏡 Current Farm Status: {farm_status}")
    return farm_status

@tool
def search_wiki(query: str):
    """
    Searches the Stardew Valley Wiki for information about crops, 
    NPCs, festivals, and game mechanics.
    Execute this tool for specific agent, only search for the related info.
    Inut: a string decribing the type of info, one of crops, animals, festivals, NPC or others.
    """
    results = collection.query(query_texts=[query], n_results=3, include=['documents'])
    if results['documents']:
        context = "\n\n".join(results['documents'][0])
        print(f"  📚 Found related Wiki context of length {len(context)} in SV Wiki")
        return f"Wiki Results for '{query}':\n{context}"
    
    print(f"  📚 No relevant Wiki found.")
    return "No relevant Wiki information found."

@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )