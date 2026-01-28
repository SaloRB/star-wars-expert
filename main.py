"""Star Wars Movie Expert - Main entry point."""

import os
import sys

from colorama import init
from dotenv import load_dotenv
from rich.console import Console

from chat import create_rag_chain, run_chat_loop
from vectorstore import get_or_create_vectorstore

# Load environment variables from .env file
load_dotenv()


def validate_environment() -> bool:
    """Validate that all required environment variables are set.

    Returns:
        True if all required variables are set, False otherwise
    """
    required_vars = {
        "OPENAI_API_KEY": "Required for OpenAI API access. Get it from https://platform.openai.com/api-keys"
    }

    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  • {var}: {description}")

    if missing_vars:
        print("\n❌ Missing required environment variables:\n")
        print("\n".join(missing_vars))
        print("\n💡 Tip: Copy .env.example to .env and fill in your values:\n")
        print("   cp .env.example .env\n")
        return False

    return True


# Validate environment before proceeding
if not validate_environment():
    sys.exit(1)

# Initialize colorama
init(autoreset=True)


def main():
    """Main application entry point."""
    console = Console()

    try:
        # Get or create vector store
        vectorstore = get_or_create_vectorstore(console)

        # Create RAG chain with conversation memory
        rag_chain, memory = create_rag_chain(vectorstore)

        # Run chat loop
        run_chat_loop(rag_chain, memory)

    except KeyboardInterrupt:
        console.print(
            "\n[magenta]Exiting the Star Wars Movie Expert. May the Force be with you![/magenta]\n"
        )
        sys.exit(0)
    except Exception as e:
        error_msg = str(e)
        console.print(f"\n[red]❌ {error_msg}[/red]")
        # Only show generic hint if error doesn't already contain guidance
        if "https://" not in error_msg and "→" not in error_msg:
            console.print("[dim]Check your internet connection and try again.[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()
