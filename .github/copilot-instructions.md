# Star Wars Expert - AI Coding Assistant Instructions

## Project Overview

This is a **local-only** RAG (Retrieval-Augmented Generation) application that answers questions about Star Wars **original trilogy scripts only** (Episodes IV-VI). The architecture follows a classic LangChain pattern: **load → chunk → embed → store → retrieve → generate**.

**Scope is fixed**: No plans to add additional movies or script sources beyond the three IMSDB scripts.

### Core Data Flow

1. [loader.py](../loader.py) - Fetches scripts from IMSDB, chunks with `RecursiveCharacterTextSplitter` using screenplay-specific separators (`\nINT.`, `\nEXT.`)
2. [vectorstore.py](../vectorstore.py) - Embeds chunks with OpenAI's `text-embedding-3-small` and stores in Qdrant (local file-based at `./qdrant_db`)
3. [chat.py](../chat.py) - Retrieves top-k chunks, manages conversation memory, and streams responses from `gpt-4o` via LangChain LCEL pipeline
4. [ui.py](../ui.py) - UI components including animated step progress display
5. [config.py](../config.py) - Centralized configuration for all constants
6. [main.py](../main.py) - Entry point that orchestrates the flow

## Key Architecture Decisions

### Why Qdrant file-based storage?

The vectorstore persists to `./qdrant_db` directory (not in-memory) to avoid re-downloading/re-embedding scripts on every run. Check existence via `client.get_collection()` before rebuilding.

### Why k=15 retriever?

Scripts are chunked at 2500 chars with 250 overlap. High k value (15 chunks) ensures context spans multiple scenes/movies for cross-episode questions.

### Why screenplay-specific separators?

`["\nINT.", "\nEXT.", "\n\n", "\n", " ", ""]` preserves scene boundaries. **Always use these separators** when modifying chunking logic - generic separators break scene context.

### Conversation Memory

Uses `ConversationMemory` class in [chat.py](../chat.py) to maintain context across exchanges:
- Stores last `MEMORY_K=5` exchanges (configurable)
- Enables pronoun resolution ("What happens to him?")
- Truncates long messages to save context window

## Development Workflow

### Environment Setup

```bash
# Uses uv for dependency management (see uv.lock)
uv sync

# Required: Create .env file with OpenAI API key
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...
```

### Running the Application

```bash
uv run main.py
# First run: Downloads scripts, creates embeddings (~30-60 sec)
# Subsequent runs: Loads from ./qdrant_db (~1 sec)
```

### Chat Commands

- `exit` / `quit` - Exit the chatbot
- `clear` - Clear conversation history

### Rebuilding Vector Store

Delete `./qdrant_db` to force re-indexing (useful after changing chunk size/overlap in [config.py](../config.py)).

## Project-Specific Conventions

### Terminal UI Patterns

- Uses `colorama` for cross-platform color (with `init(autoreset=True)`)
- Uses `rich` for animated step progress during initialization (see [ui.py](../ui.py))
- Implements streaming with typing effect: `TYPING_DELAY=0.03` (30ms per character)
- Responses include 3 suggested follow-up questions formatted with custom separator `─────────────────────────────────────────`

### Prompt Engineering Structure

The `PROMPT_TEMPLATE` in [config.py](../config.py) is critical:

- Enforces "scripts-only" grounding (refuses off-topic questions)
- Requires quoting dialogue when relevant
- Uses conversation history for context (`{chat_history}` placeholder)
- Auto-generates 3 follow-up questions with `🔍 Related questions` format

**Never remove these constraints** - they prevent hallucination about non-canonical content.

### Configuration Pattern

All constants live in [config.py](../config.py):

| Constant | Description |
|----------|-------------|
| `LLM_MODEL` | OpenAI model (gpt-4o) |
| `EMBEDDING_MODEL` | Embedding model (text-embedding-3-small) |
| `RETRIEVER_K` | Number of chunks to retrieve (15) |
| `MEMORY_K` | Conversation turns to remember (5) |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | Text splitter settings |
| `TYPING_DELAY` | Typing effect speed (0.03s) |
| `SPINNER_FRAMES` | Animation frames for progress spinner |
| `STAR_WARS_SCRIPTS` | List of script URLs |
| `PROMPT_TEMPLATE` | System prompt |

## Common Modification Scenarios

### Changing Chunk Size

Modify `CHUNK_SIZE` / `CHUNK_OVERLAP` in [config.py](../config.py). Delete `./qdrant_db` and re-run to rebuild. Test with `RETRIEVER_K=15` - may need adjustment if chunks get much larger/smaller.

### Switching Embedding Model

Update `EMBEDDING_MODEL` in [config.py](../config.py) and rebuild vector store (different embeddings = incompatible).

### Adjusting Response Style

Edit `PROMPT_TEMPLATE` in [config.py](../config.py). The separator format (`─────`) and question prefix (`▸`) are parsed in [chat.py](../chat.py) - keep format consistent.

### Adjusting Conversation Memory

Modify `MEMORY_K` in [config.py](../config.py) to change how many exchanges are remembered. Higher values use more tokens.

## External Dependencies

- **IMSDB (imsdb.com)**: Scripts scraped from `<pre>` tags. If site structure changes, update BeautifulSoup selector in [loader.py](../loader.py).
- **OpenAI API**: Both embeddings and chat completions. Rate limits apply to initial indexing.
- **Qdrant**: Local file-based client. No server required, but `./qdrant_db` grows ~5-10MB per script.

## Testing

The project includes comprehensive tests using pytest:

```bash
# Run unit tests (fast, no API calls)
uv run pytest tests/ -m "not integration"

# Run integration tests (uses OpenAI API)
uv run pytest tests/ -m integration

# Run all tests with verbose output
uv run pytest tests/ -v
```

### Test Structure

- `tests/test_config.py` - Validates configuration constants
- `tests/test_loader.py` - Tests script loading with mocked HTTP
- `tests/test_rag_integration.py` - End-to-end RAG tests (requires API key)

### Manual Test Cases

- **Cross-movie questions**: "How does Luke's character evolve?" (should cite all 3 movies)
- **Grounding test**: "Who is Rey?" (should refuse - not in original trilogy)
- **Conversation memory**: Ask about Luke, then "What happens to him?" (should resolve pronoun)
- **Edge cases**: Very long questions, typos in character names

### Debugging Tips

- Print `context` variable in [chat.py](../chat.py) before prompt to inspect retrieved chunks
- Check `./qdrant_db/collection/star_wars_scripts/` for vector count after indexing
- Use lower `RETRIEVER_K` temporarily to see which chunks are most relevant
- Check `memory.get_history_string()` to inspect conversation context
