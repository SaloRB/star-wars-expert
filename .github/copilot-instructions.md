# Star Wars Expert - AI Coding Assistant Instructions

## Project Overview

This is a **local-only** RAG (Retrieval-Augmented Generation) application that answers questions about Star Wars **original trilogy scripts only** (Episodes IV-VI). The architecture follows a classic LangChain pattern: **load → chunk → embed → store → retrieve → generate**.

**Scope is fixed**: No plans to add additional movies or script sources beyond the three IMSDB scripts.

### Core Data Flow

1. [loader.py](../loader.py) - Fetches scripts from IMSDB, chunks with `RecursiveCharacterTextSplitter` using screenplay-specific separators (`\nINT.`, `\nEXT.`)
2. [vectorstore.py](../vectorstore.py) - Embeds chunks with OpenAI's `text-embedding-3-small` and stores in Qdrant (local file-based at `./qdrant_db`)
3. [chat.py](../chat.py) - Retrieves top-k=15 chunks and streams responses from `gpt-4o` via LangChain LCEL pipeline
4. [main.py](../main.py) - Entry point that orchestrates the flow

## Key Architecture Decisions

### Why Qdrant file-based storage?

The vectorstore persists to `./qdrant_db` directory (not in-memory) to avoid re-downloading/re-embedding scripts on every run. Check existence via `client.get_collection()` before rebuilding.

### Why k=15 retriever?

Scripts are chunked at 2500 chars with 250 overlap. High k value (15 chunks) ensures context spans multiple scenes/movies for cross-episode questions.

### Why screenplay-specific separators?

`["\nINT.", "\nEXT.", "\n\n", "\n", " ", ""]` preserves scene boundaries. **Always use these separators** when modifying chunking logic - generic separators break scene context.

## Development Workflow

### Environment Setup

```bash
# Uses uv for dependency management (see uv.lock)
uv sync

# Required: Set OpenAI API key (before running)
export OPENAI_API_KEY='sk-...'

# Alternative: Use .env file with python-dotenv for convenience
# Create .env: echo "OPENAI_API_KEY=sk-..." > .env
# Add to pyproject.toml: python-dotenv>=1.0.0
# Load in main.py: from dotenv import load_dotenv; load_dotenv()
```

### Running the Application

```bash
python main.py
# First run: Downloads scripts, creates embeddings (~2-3 min)
# Subsequent runs: Loads from ./qdrant_db (~2 sec)
```

### Rebuilding Vector Store

Delete `./qdrant_db` to force re-indexing (useful after changing chunk size/overlap in [config.py](../config.py)).

## Project-Specific Conventions

### Terminal UI Patterns

- Uses `colorama` for cross-platform color (with `init(autoreset=True)`)
- Uses `rich` for progress bars during script loading
- Implements streaming with typing effect: 50ms delay per character in [chat.py](../chat.py#L65)
- Responses include 3 suggested follow-up questions formatted with custom separator `─────────────────────────────────────────`

### Prompt Engineering Structure

The `PROMPT_TEMPLATE` in [config.py](../config.py) is critical:

- Enforces "scripts-only" grounding (refuses off-topic questions)
- Requires quoting dialogue when relevant
- Auto-generates 3 follow-up questions with `🔍 Related questions` format

**Never remove these constraints** - they prevent hallucination about non-canonical content.

### Configuration Pattern

All constants live in [config.py](../config.py):

- `STAR_WARS_SCRIPTS`: List of dicts with `title` and `url`
- `PERSIST_PATH` / `COLLECTION_NAME`: Qdrant config
- `PROMPT_TEMPLATE`: Single source of truth for system prompt

**Note**: The original trilogy script list is considered complete and stable. No additional movies are planned.

## Common Modification Scenarios

### Changing Chunk Size

Modify `chunk_size` / `chunk_overlap` in [loader.py](../loader.py#L32-L33). Test with `k=15` retrieval - may need adjustment if chunks get much larger/smaller.

### Switching Embedding Model

Update `OpenAIEmbeddings(model="...")` in [vectorstore.py](../vectorstore.py#L17) and rebuild vector store (different embeddings = incompatible).

### Adjusting Response Style

Edit `PROMPT_TEMPLATE` in [config.py](../config.py). The separator format (`─────`) and question prefix (`▸`) are parsed in [chat.py](../chat.py#L51-L56) - keep format consistent.

## External Dependencies

- **IMSDB (imsdb.com)**: Scripts scraped from `<pre>` tags. If site structure changes, update [loader.py](../loader.py#L26-L29) BeautifulSoup selector.
- **OpenAI API**: Both embeddings and chat completions. Rate limits apply to initial indexing (dozens of embed calls).
- **Qdrant**: Local file-based client. No server required, but `./qdrant_db` grows ~5-10MB per script.

## Testing and Debugging

**No formal test suite** - this is a local-only project optimized for quick iteration. Manual testing is sufficient:

### Manual Test Cases

- **Cross-movie questions**: "How does Luke's character evolve?" (should cite all 3 movies)
- **Grounding test**: "Who is Rey?" (should refuse - not in original trilogy)
- **Retrieval quality**: Questions about minor characters should still find relevant chunks if k=15 works
- **Edge cases**: Very long questions, typos in character names, questions about deleted scenes

### Optional: Add Basic Tests

If adding pytest for key components:

```bash
# Add to pyproject.toml dependencies
pytest>=8.0.0
pytest-mock>=3.12.0

# Test loader.py: Mock requests.get() to avoid IMSDB dependency
# Test vectorstore.py: Verify collection creation/loading logic
# Test chat.py: Check separator parsing for follow-up questions
```

### Debugging Tips

- Print `context` variable in [chat.py](../chat.py) before prompt to inspect retrieved chunks
- Check `./qdrant_db/collection/star_wars_scripts/` for vector count after indexing
- Use `k=3` temporarily to see which chunks are most relevant for a query
