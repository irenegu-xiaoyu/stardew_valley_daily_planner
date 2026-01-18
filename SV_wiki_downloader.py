import requests
import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB (Local)
client = chromadb.PersistentClient(path="./stardew_knowledge")
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

try:
    client.delete_collection(name="stardew_wiki")
    print("🗑️ Old data cleared. Starting fresh!")
except:
    print("✨ No existing data found. Creating new collection.")

collection = client.get_or_create_collection(name="stardew_wiki", embedding_function=embed_fn)

WIKI_API = "https://stardewvalleywiki.com/mediawiki/api.php"

def scrape_and_store(page_list):

    headers = {
        'User-Agent': 'StardewValleyDailySchedulerBot/1.0 Stardew Scholar Project'
    }

    for page in page_list:
        print(f"Start downloading page: {page}")

        params = {
            "action": "parse", "format": "json", "page": page,
            "prop": "wikitext", "redirects": 1
        }
        data = requests.get(WIKI_API, params=params, headers=headers).json()

        if 'parse' in data:
            content = data["parse"]["wikitext"]["*"]
            print(f"✅ Success! Found '{page}'. Length: {len(content)}")
        else:
            print(f"❌ Downloading wiki failed for {page}")
            return 


        # Chunking: Split by double-newlines to keep paragraphs together
        chunks = [c.strip() for c in content.split('\n\n') if len(c) > 60]

        
        # Add to Vector DB
        collection.add(
            documents=chunks,
            ids=[f"{page}_{i}" for i in range(len(chunks))],
            metadatas=[{"source": page}] * len(chunks)
        )
        print(f"✅ Ingested {page} ({len(chunks)} chunks)")

# Download essential pages for now
essential_pages = [
    # essentials
    "Crops", "Fish", "Villagers",
    # daily planning
    "Bundles", "Weather", "Luck", "Calendar",
    # money making
    "Artisan_Goods", "Pierre's_General_Store", "Carpenter's_Shop", "Marnie's_Ranch", "Shipping",
    # asset 
    "Fishing_Strategy", "The_Mines",
    # social
    "Friendship", 
    # "Schedules" failed for now, 
]

# In future we may want to download more info
# "Foraging", "Crafting", "Cooking", "Tools", "Festivals", "Ginger_Island"

scrape_and_store(essential_pages)

