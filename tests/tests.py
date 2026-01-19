import chromadb
from chromadb.utils import embedding_functions

# Connect to your local DB
client = chromadb.PersistentClient(path="./stardew_knowledge")
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="stardew_wiki", embedding_function=embed_fn)

def testSearchCropsData():

    # Let's see if the 'Crops' data we just pulled is actually searchable
    query_text = "How many days does it take for Cauliflower to grow?"
    results = collection.query(
        query_texts=[query_text],
        n_results=2
    )

    print("\n🔎 RAG Search Results:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"\nChunk {i+1}:")
        print(doc[:200] + "...") # Print first 200 characters of the match

testSearchCropsData()