"""RAG chain and chat interface for Star Wars Expert."""

import sys
import time
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from colorama import Fore, Style

from config import PROMPT_TEMPLATE


def create_rag_chain(vectorstore: QdrantVectorStore):
    """Create a RAG chain for answering questions about Star Wars scripts.

    Args:
        vectorstore: The vector store containing script chunks

    Returns:
        Configured RAG chain
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 15})
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def run_chat_loop(rag_chain):
    """Run the interactive chat loop.

    Args:
        rag_chain: The configured RAG chain
    """
    print(f"\n{Fore.YELLOW}{'='*70}")
    print(f"{Fore.YELLOW}🌟  The Star Wars Movie Expert is ready to answer your questions  🌟")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")

    while True:
        query = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
        if query.lower() in ["exit", "quit"]:
            print(
                f"\n{Fore.MAGENTA}Exiting the Star Wars Movie Expert. May the Force be with you!{Style.RESET_ALL}\n")
            break

        # Accumulate the full response
        full_response = ""
        for chunk in rag_chain.stream(query):
            full_response += chunk

        # Split response from suggestions
        separator = "─────────────────────────────────────────"
        if separator in full_response:
            main_answer, suggestions = full_response.split(separator, 1)
            suggestions = separator + suggestions
        else:
            main_answer = full_response
            suggestions = ""

        # Print main answer with typing effect
        print(f"\n{Fore.BLUE}Star Wars Movie Expert:{Style.RESET_ALL} ", end="")
        sys.stdout.flush()

        for char in main_answer:
            print(char, end="", flush=True)
            time.sleep(0.05)  # Delay de 50ms por caracter

        # Print suggestions in yellow color if they exist
        if suggestions:
            print(f"\n{Fore.YELLOW}{suggestions}{Style.RESET_ALL}", end="")

        print("\n")
