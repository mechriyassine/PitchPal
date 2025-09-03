from sentence_transformers import SentenceTransformer
import chromadb
import os
import logging
from dotenv import load_dotenv
load_dotenv()

LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH")
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def embed_and_store_headlines(headlines, collection_name="football_headlines"):
    """Embed headlines using Sentence Transformers and store in ChromaDB."""
    try:
        # Load a pre-trained sentence transformer model
        logger.info("Loading SentenceTransformer model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

        # Define the full path to the ChromaDB storage directory
        persist_path = os.path.abspath(os.path.join("chroma_db"))
        logger.info(f"ChromaDB storage path: {persist_path}")

        # Create the directory if it doesn't exist
        os.makedirs(persist_path, exist_ok=True)

        # Use PersistentClient with the correct path
        client = chromadb.PersistentClient(path=persist_path)
        collection = client.get_or_create_collection(collection_name)

        # Embed headlines and add to the collection in batch
        logger.info(f"Embedding {len(headlines)} headlines...")
        embeddings = model.encode(headlines).tolist()
        collection.add(
            documents=headlines,
            embeddings=embeddings,
            ids=[str(i) for i in range(len(headlines))]
        )
        logger.info(f"Stored {len(headlines)} headlines in ChromaDB.")
    except Exception as e:
        logger.error(f"Error in embed_and_store_headlines: {e}")
        raise

def query_headlines(query, collection_name="football_headlines", n_results=5):
    """Query ChromaDB for headlines matching the input query."""
    try:
        # Load SentenceTransformer model
        logger.info("Loading SentenceTransformer model for query...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

        # Connect to ChromaDB
        persist_path = os.path.abspath(os.path.join("chroma_db"))
        client = chromadb.PersistentClient(path=persist_path)
        collection = client.get_or_create_collection(collection_name)

        # Embed the query
        logger.info(f"Embedding query: {query}")
        query_embedding = model.encode([query]).tolist()

        # Query the collection
        results = collection.query(query_embeddings=query_embedding, n_results=n_results)
        logger.info(f"Retrieved {len(results['documents'][0])} headlines for query")
        return results["documents"][0]
    except Exception as e:
        logger.error(f"Error in query_headlines: {e}")
        return []

def generate_answer(query, collection_name="football_headlines", n_results=5):
    headlines = query_headlines(query, collection_name, n_results)
    context = "\n".join(headlines)
    prompt = f"Using these headlines:\n{context}\nAnswer this question: {query}"
    try:
        from llama_cpp import Llama
        llm = Llama(model_path=LLAMA_MODEL_PATH)
        output = llm(prompt, max_tokens=256)
        logger.info(f"Prompt sent to LLM: {prompt}")
        logger.info(f"LLM raw output: {output}")
        # Try all possible output formats
        if isinstance(output, dict) and "choices" in output:
            return output["choices"][0]["text"].strip()
        elif hasattr(output, "text"):
            return output.text.strip()
        elif isinstance(output, str):
            return output.strip()
        else:
            return str(output)
    except Exception as e:
        logger.error(f"Error in generate_answer (LLM): {e}")
        return "Sorry, I couldn't generate an answer."

if __name__ == "__main__":
    try:
        # Load headlines from file and store
        with open("headlines.txt", "r", encoding="utf-8") as f:
            headlines = [line.strip().split(". ", 1)[-1] for line in f if line.strip()]
        embed_and_store_headlines(headlines)

        # Test query functionality
        test_query = "football transfer news"
        logger.info(f"Testing query: {test_query}")
        results = query_headlines(test_query)
        if results:
            print(f"Query: {test_query}")
            for idx, headline in enumerate(results, 1):
                print(f"{idx}. {headline}")
        else:
            print("No results found for test query.")
    except Exception as e:
        logger.error(f"Error in main: {e}")