"""Star Wars Movie Expert - Main entry point."""

from dotenv import load_dotenv
from colorama import init
from rich.console import Console

from vectorstore import get_or_create_vectorstore
from chat import create_rag_chain, run_chat_loop

# Load environment variables from .env file
load_dotenv()

# Initialize colorama
init(autoreset=True)


def main():
    """Main application entry point."""
    console = Console()

    # Get or create vector store
    vectorstore = get_or_create_vectorstore(console)

    # Create RAG chain
    rag_chain = create_rag_chain(vectorstore)

    # Run chat loop
    run_chat_loop(rag_chain)


if __name__ == "__main__":
    main()
