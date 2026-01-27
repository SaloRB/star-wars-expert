# 🌟 Star Wars Expert

A RAG-powered chatbot that answers questions about the Star Wars original trilogy using actual movie scripts.

## Description

This project uses LangChain and Qdrant to create an intelligent assistant that can answer questions about Star Wars by retrieving relevant context from the actual movie scripts (A New Hope, The Empire Strikes Back, Return of the Jedi).

## Installation

```bash
# Clone the repository
git clone https://github.com/SaloRB/star-wars-expert.git
cd star-wars-expert

# Install dependencies with uv
uv sync
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

```bash
uv run main.py
```

The chatbot will:
1. Download and process the Star Wars scripts (first run only)
2. Create a vector database for semantic search
3. Start an interactive chat session

## Features

- 🎬 Uses actual movie scripts from the original trilogy
- 🔍 Semantic search with Qdrant vector database
- 💬 Interactive chat with streaming responses
- 🎨 Beautiful terminal UI with colors and typing effects
- ⚡ Automatic retry on network errors
- ✅ Environment validation on startup

## Project Structure

```
star-wars-expert/
├── main.py           # Entry point
├── config.py         # Centralized configuration
├── loader.py         # Script fetching and processing
├── vectorstore.py    # Qdrant vector store management
├── chat.py           # RAG chain and chat interface
└── tests/            # Unit and integration tests
```

## Configuration Options

All configuration is centralized in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `LLM_MODEL` | `gpt-4o` | OpenAI model to use |
| `LLM_TEMPERATURE` | `0` | Model temperature |
| `RETRIEVER_K` | `15` | Number of chunks to retrieve |
| `CHUNK_SIZE` | `2500` | Text chunk size |
| `CHUNK_OVERLAP` | `250` | Overlap between chunks |

## Testing

```bash
# Run unit tests (fast, no API calls)
uv run pytest tests/ -m "not integration"

# Run integration tests (uses OpenAI API)
uv run pytest tests/ -m integration

# Run all tests
uv run pytest tests/ -v
```

## Requirements

- Python 3.10+
- OpenAI API key

## License

MIT