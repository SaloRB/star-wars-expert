"""Vector store management for Star Wars scripts."""

import time
import threading
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from rich.console import Console
from rich.panel import Panel
from rich.live import Live

from config import PERSIST_PATH, COLLECTION_NAME, EMBEDDING_MODEL, SPINNER_FRAMES
from loader import load_and_split_scripts


def create_step_display(steps: list[tuple[str, str]], spinner_frame: int = 0) -> Panel:
    """Create a panel showing progress steps."""
    lines = []
    for i, (desc, status) in enumerate(steps):
        if status == "done":
            marker = "[green]✓[/green]"
        elif status == "running":
            marker = f"[cyan]{SPINNER_FRAMES[spinner_frame % len(SPINNER_FRAMES)]}[/cyan]"
        else:  # pending
            marker = "[dim]○[/dim]"
        
        step_num = f"[dim][{i+1}/{len(steps)}][/dim]"
        lines.append(f"   {step_num} {desc:<30} {marker}")
    
    content = "\n".join(lines)
    return Panel(content, title="[bold cyan]🚀 Initializing Star Wars Expert[/bold cyan]", border_style="cyan")


class StepProgress:
    """Manages step-by-step progress with animated spinner."""
    
    def __init__(self, console: Console, steps: list[str]):
        self.console = console
        self.steps = [(s, "pending") for s in steps]
        self.current_step = -1
        self.spinner_frame = 0
        self.running = False
        self.live = None
        self._spinner_thread = None
    
    def start(self):
        """Start the progress display."""
        self.live = Live(create_step_display(self.steps), console=self.console, refresh_per_second=10)
        self.live.start()
        self.running = True
        self._spinner_thread = threading.Thread(target=self._animate_spinner, daemon=True)
        self._spinner_thread.start()
    
    def _animate_spinner(self):
        """Animate the spinner in background."""
        while self.running:
            time.sleep(0.1)
            self.spinner_frame += 1
            if self.live:
                self.live.update(create_step_display(self.steps, self.spinner_frame))
    
    def advance(self):
        """Mark current step as done and move to next."""
        if self.current_step >= 0:
            desc = self.steps[self.current_step][0]
            self.steps[self.current_step] = (desc, "done")
        
        self.current_step += 1
        if self.current_step < len(self.steps):
            desc = self.steps[self.current_step][0]
            self.steps[self.current_step] = (desc, "running")
        
        if self.live:
            self.live.update(create_step_display(self.steps, self.spinner_frame))
    
    def complete(self, message: str = ""):
        """Complete all steps and stop."""
        # Mark all remaining as done
        for i in range(len(self.steps)):
            desc = self.steps[i][0]
            self.steps[i] = (desc, "done")
        
        self.running = False
        if self.live:
            self.live.update(create_step_display(self.steps, self.spinner_frame))
            self.live.stop()
        
        if message:
            self.console.print(message)


def get_or_create_vectorstore(console: Console) -> QdrantVectorStore:
    """Get existing vector store or create a new one from scripts."""
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
