"""RAG chain and chat interface for Star Wars Expert."""

import sys
import time
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_qdrant import QdrantVectorStore
from colorama import Fore, Style

from config import PROMPT_TEMPLATE, LLM_MODEL, LLM_TEMPERATURE, RETRIEVER_K, MEMORY_K, TYPING_DELAY


class ConversationMemory:
    """Simple conversation memory that stores the last K exchanges."""
    
    def __init__(self, k: int = 5):
        self.k = k
        self.messages: list[HumanMessage | AIMessage] = []
    
    def add_user_message(self, content: str):
        """Add a user message to memory."""
        self.messages.append(HumanMessage(content=content))
        self._trim()
    
    def add_ai_message(self, content: str):
        """Add an AI message to memory."""
        self.messages.append(AIMessage(content=content))
        self._trim()
    
    def _trim(self):
        """Keep only the last K exchanges (2K messages)."""
        max_messages = self.k * 2
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]
    
    def get_history_string(self) -> str:
        """Get conversation history as a formatted string."""
        if not self.messages:
            return "No previous conversation."
        
        history_parts = []
        for msg in self.messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            # Truncate long messages to save context
            content = msg.content[:500] + "..." if len(msg.content) > 500 else msg.content
            history_parts.append(f"{role}: {content}")
        
        return "\n".join(history_parts)
    
    def clear(self):
        """Clear conversation history."""
        self.messages = []


def create_rag_chain(vectorstore: QdrantVectorStore):
    """Create a RAG chain for answering questions about Star Wars scripts.

    Args:
        vectorstore: The vector store containing script chunks

    Returns:
        Tuple of (RAG chain, ConversationMemory)
    """
    llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE, streaming=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Create conversation memory
    memory = ConversationMemory(k=MEMORY_K)
    
    def get_context_and_history(query: str) -> dict:
        """Get context from retriever and history from memory."""
        context = retriever.invoke(query)
        return {
            "context": context,
            "chat_history": memory.get_history_string(),
            "question": query
        }

    rag_chain = (
        RunnableLambda(get_context_and_history)
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, memory


def run_chat_loop(rag_chain, memory: ConversationMemory):
    """Run the interactive chat loop.

    Args:
        rag_chain: The configured RAG chain
        memory: The conversation memory
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
        
        if query.lower() == "clear":
            memory.clear()
            print(f"{Fore.CYAN}Conversation history cleared.{Style.RESET_ALL}\n")
            continue

        # Add user message to memory
        memory.add_user_message(query)

        # Accumulate the full response
        full_response = ""
        for chunk in rag_chain.stream(query):
            full_response += chunk

        # Add AI response to memory (without suggestions)
        separator = "─────────────────────────────────────────"
        if separator in full_response:
            main_answer, suggestions = full_response.split(separator, 1)
            suggestions = separator + suggestions
        else:
            main_answer = full_response
            suggestions = ""
        
        # Store main answer in memory (without suggestions)
        memory.add_ai_message(main_answer.strip())

        # Print main answer with typing effect
        print(f"\n{Fore.BLUE}Star Wars Movie Expert:{Style.RESET_ALL} ", end="")
        sys.stdout.flush()

        for char in main_answer:
            print(char, end="", flush=True)
            time.sleep(TYPING_DELAY)  # Configurable typing effect delay

        # Print suggestions in yellow color if they exist
        if suggestions:
            print(f"\n{Fore.YELLOW}{suggestions}{Style.RESET_ALL}", end="")

        print("\n")
