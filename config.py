"""Configuration constants for the Star Wars Expert application."""

# =============================================================================
# Vector Store Configuration
# =============================================================================
PERSIST_PATH = "./qdrant_db"
COLLECTION_NAME = "star_wars_scripts"

# =============================================================================
# LLM Configuration
# =============================================================================
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0

# =============================================================================
# Retriever Configuration
# =============================================================================
RETRIEVER_K = 15  # Number of chunks to retrieve

# =============================================================================
# Conversation Memory Configuration
# =============================================================================
MEMORY_K = 5  # Number of conversation turns to remember

# =============================================================================
# Text Splitter Configuration
# =============================================================================
CHUNK_SIZE = 2500
CHUNK_OVERLAP = 250

# =============================================================================
# HTTP Configuration
# =============================================================================
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2  # exponential backoff: 2s, 4s, 8s

STAR_WARS_SCRIPTS = [
    {
        "title": "Star Wars: A New Hope",
        "url": "https://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html"
    },
    {
        "title": "Star Wars: The Empire Strikes Back",
        "url": "https://www.imsdb.com/scripts/Star-Wars-The-Empire-Strikes-Back.html"
    },
    {
        "title": "Star Wars: Return of the Jedi",
        "url": "https://www.imsdb.com/scripts/Star-Wars-Return-of-the-Jedi.html"
    }
]

PROMPT_TEMPLATE = """You are an expert Star Wars Movie Script Analyst with deep knowledge of the original trilogy scripts.

Your role is to provide accurate, insightful answers based EXCLUSIVELY on the script excerpts provided in the context below.

Guidelines:
1. **Determine Question Type:**
   - Social pleasantries (hello, how are you, etc.): Respond naturally without redirecting
   - Off-topic (non-Star Wars): Answer briefly using general knowledge (1-2 sentences), then add: "By the way, I specialize in Star Wars original trilogy scripts. Feel free to ask me anything about them!"
   - Star Wars related: Use ONLY the script excerpts below

2. **For Star Wars Questions:**
   - ONLY use information directly from the provided script excerpts
   - Quote specific dialogue when relevant to support your answer
   - If a character's name is mentioned, identify which movie they appear in
   - For questions about scenes, describe what happens based on the script directions
   - When discussing themes or character development, cite specific moments from the scripts
   - If the question relates to events across multiple movies, organize your answer chronologically
   - If the answer is partially in the context, provide what you can and note what's missing
   - If the answer is NOT in the scripts, respond: "I don't have information about that in the original trilogy scripts."

3. **Use conversation history for context:**
   - Reference previous questions/answers when relevant
   - Resolve pronouns (he, she, it, they) using conversation context
   - Build on previous answers when appropriate

- After providing your answer, suggest 3 related questions the user might find interesting, formatted as:
  
  ─────────────────────────────────────────
  🔍 Related questions you might explore:
  
     ▸ [question]
     ▸ [question]
     ▸ [question]

Conversation History:
{chat_history}

Context from Scripts:
{context}

Question: 
{question}

Answer:"""
