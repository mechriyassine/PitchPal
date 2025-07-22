Set Up Your Python Project [x]
 - Create a new Python project folder. [x]
 - Set up a virtual environment. [x]

Install Essential Packages [x]
 - requests, beautifulsoup4 (for scraping)
 - pandas (for data handling)
 - sentence-transformers or similar (for embeddings)
 - chromadb or faiss (for vector DB)
 - llama-cpp-python (for LLM, or use API)
 - streamlit or fastapi (for web UI)

Build a Simple Web Scraper
 - Start by scraping football news or stats from a site like transfermarkt, whoscored, or a news blog.
 - Extract titles, articles, player names, stats, etc.

Process and Store Data
 - Clean and chunk the scraped text.
 - Store chunks with metadata (source, date, player/team, etc.)

Embed and Index Data
 - Use a sentence transformer to create embeddings for each chunk.
 - Store embeddings in a vector database.

Build the RAG Pipeline
 - Retrieve relevant chunks for a user’s question.
 - Pass them to the LLM to generate an answer.

Create a Simple UI
 - Let users enter questions and see answers with sources.