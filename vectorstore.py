"""Vector store management for Star Wars scripts."""

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from rich.console import Console

from config import PERSIST_PATH, COLLECTION_NAME
from loader import load_and_split_scripts


def get_or_create_vectorstore(console: Console) -> QdrantVectorStore:
    """Get existing vector store or create a new one from scripts.

    Args:
        console: Rich console for displaying progress

    Returns:
        Configured QdrantVectorStore instance
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    client = QdrantClient(path=PERSIST_PATH)

    try:
        client.get_collection(collection_name=COLLECTION_NAME)
        vectorstore = QdrantVectorStore(
            collection_name=COLLECTION_NAME,
            embedding=embeddings,
            client=client,
        )
    except Exception:
        client.close()

        # Load and split scripts
        all_chunks = load_and_split_scripts(console)

        # Create new vector store
        vectorstore = QdrantVectorStore.from_documents(
            all_chunks,
            embedding=embeddings,
            path=PERSIST_PATH,
            collection_name=COLLECTION_NAME,
        )

    return vectorstore
