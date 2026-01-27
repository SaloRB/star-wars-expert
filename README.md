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

```env
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

### Chat Commands

| Command | Description |
|---------|-------------|
| `exit` / `quit` | Exit the chatbot |
| `clear` | Clear conversation history |

## Features

- 🎬 Uses actual movie scripts from the original trilogy
- 🔍 Semantic search with Qdrant vector database
- 💬 Interactive chat with streaming responses
- 🧠 Conversation memory (remembers last 5 exchanges)
- 🎨 Beautiful terminal UI with animated progress
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
├── ui.py             # UI components (progress display)
└── tests/            # Unit and integration tests
```

## Configuration Options

All configuration is centralized in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `LLM_MODEL` | `gpt-4o` | OpenAI model to use |
| `LLM_TEMPERATURE` | `0` | Model temperature |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `RETRIEVER_K` | `15` | Number of chunks to retrieve |
| `MEMORY_K` | `5` | Conversation turns to remember |
| `CHUNK_SIZE` | `2500` | Text chunk size |
| `CHUNK_OVERLAP` | `250` | Overlap between chunks |
| `TYPING_DELAY` | `0.03` | Typing effect speed (seconds) |

## Testing

```bash
# Run unit tests (fast, no API calls)
uv run pytest tests/ -m "not integration"

# Run integration tests (uses OpenAI API)
uv run pytest tests/ -m integration

# Run all tests
uv run pytest tests/ -v
```

## Documentation

Complete documentation is available in the [`/docs`](./docs/) directory:

- **[Functional Documentation](./docs/DOCUMENTACION_FUNCIONAL.md)** — User stories, flows, acceptance criteria
- **[Technical Architecture](./docs/ARQUITECTURA_TECNICA.md)** — Components, integrations, data model
- **[Quality & Operations](./docs/CALIDAD_Y_OPERACION.md)** — Testing, runbooks, roadmap
- **[AI Support Knowledge Base](./docs/support/)** — FAQ, playbooks for support agents

## Requirements

- Python 3.10+
- OpenAI API key

## License

MIT
