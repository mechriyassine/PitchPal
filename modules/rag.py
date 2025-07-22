from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

def embed_and_store_headlines(headlines, collection_name="football_headlines"):
    # Load a pre-trained sentence transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create or load a ChromaDB collection
    client = chromadb.Client(Settings())
    collection = client.get_or_create_collection(collection_name)

    # Embed headlines and add to the collection
    embeddings = model.encode(headlines).tolist()
    for idx, (headline, embedding) in enumerate(zip(headlines, embeddings)):
        collection.add(
            documents=[headline],
            embeddings=[embedding],
            ids=[str(idx)]
        )
    print(f"Stored {len(headlines)} headlines in ChromaDB.")

if __name__ == "__main__":
    # Example usage: load headlines from file and store
    with open("headlines.txt", "r", encoding="utf-8") as f:
        headlines = [line.strip().split(". ", 1)[-1] for line in f if line.strip()]
    embed_and_store_headlines(headlines)