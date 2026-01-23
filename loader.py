"""Script loader for fetching and processing Star Wars scripts."""

import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.console import Console

from config import STAR_WARS_SCRIPTS


def load_star_wars_script(url: str, movie_title: str) -> Document:
    """Load a Star Wars script from a URL.

    Args:
        url: The URL of the script
        movie_title: The title of the movie

    Returns:
        A Document containing the script content and metadata

    Raises:
        ValueError: If no <pre> tag is found in the HTML
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pre_tag = soup.find('pre')
    if pre_tag is None:
        raise ValueError("No <pre> tag found in the HTML content.")
    script_raw = pre_tag.get_text()

    return Document(page_content=script_raw, metadata={"title": movie_title})


def load_and_split_scripts(console: Console) -> list[Document]:
    """Load and split all Star Wars scripts into chunks.

    Args:
        console: Rich console for displaying progress

    Returns:
        List of document chunks
    """
    script_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        add_start_index=True,
        separators=["\nINT.", "\nEXT.", "\n\n", "\n", " ", ""]
    )

    all_chunks = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            "[cyan]Loading Star Wars scripts...", total=len(STAR_WARS_SCRIPTS))

        for script in STAR_WARS_SCRIPTS:
            progress.update(
                task, description=f"[cyan]Loading {script['title']}...")
            doc = load_star_wars_script(script["url"], script["title"])
            chunks = script_splitter.split_documents([doc])
            all_chunks.extend(chunks)
            progress.advance(task)

    console.print(
        f"[green]✓[/green] Successfully loaded {len(STAR_WARS_SCRIPTS)} scripts with {len(all_chunks)} total chunks.")

    return all_chunks
