"""Vector store management for Star Wars scripts."""

import time
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from rich.console import Console

from config import PERSIST_PATH, COLLECTION_NAME, EMBEDDING_MODEL
from loader import load_and_split_scripts
from ui import StepProgress


def get_or_create_vectorstore(console: Console) -> QdrantVectorStore:
    """Get existing vector store or create a new one from scripts.

    Args:
        console: Rich console for displaying progress

    Returns:
        Configured QdrantVectorStore instance
        
    Raises:
        RuntimeError: If the vector store cannot be accessed or created
    """
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    client = QdrantClient(path=PERSIST_PATH)

    try:
        client.get_collection(collection_name=COLLECTION_NAME)
        console.print(f"[green]✓[/green] Found existing vector store: [cyan]{COLLECTION_NAME}[/cyan]")
        
        vectorstore = QdrantVectorStore(
            collection_name=COLLECTION_NAME,
            embedding=embeddings,
            client=client,
        )
        
    except ValueError:
        client.close()
        
        progress = StepProgress(console, [
            "Loading scripts...",
            "Generating embeddings...",
            "Creating vector store...",
        ])
        
        start_time = time.time()
        progress.start()
        
        # Step 1: Load scripts
        progress.advance()
        all_chunks = load_and_split_scripts(console)
        
        # Step 2 & 3: Generate embeddings and create vector store
        progress.advance()
        vectorstore = QdrantVectorStore.from_documents(
            all_chunks,
            embedding=embeddings,
            path=PERSIST_PATH,
            collection_name=COLLECTION_NAME,
        )
        progress.advance()
        
        elapsed = time.time() - start_time
        progress.complete(f"\n[green]✓[/green] Ready! [dim](loaded {len(all_chunks)} chunks in {elapsed:.1f}s)[/dim]\n")
        
    except Exception as e:
        client.close()
        raise RuntimeError(f"Failed to access vector store: {e}") from e

    return vectorstore
