"""Script loader for fetching and processing Star Wars scripts."""

import time

import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout
from rich.console import Console

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    RETRY_BACKOFF_FACTOR,
    STAR_WARS_SCRIPTS,
)


def load_star_wars_script(url: str, movie_title: str, console: Console | None = None) -> Document:
    """Load a Star Wars script from a URL with retry logic.

    Args:
        url: The URL of the script
        movie_title: The title of the movie
        console: Optional Rich console for displaying messages

    Returns:
        A Document containing the script content and metadata

    Raises:
        RuntimeError: If the request fails after all retries
        ValueError: If no <pre> tag is found in the HTML
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes

            soup = BeautifulSoup(response.content, "html.parser")
            pre_tag = soup.find("pre")

            if pre_tag is None:
                raise ValueError(f"No <pre> tag found in the HTML content for {movie_title}")

            script_raw = pre_tag.get_text()
            return Document(page_content=script_raw, metadata={"title": movie_title})

        except Timeout:
            if console:
                console.print(
                    f"[yellow]⚠ Timeout loading {movie_title} (attempt {attempt}/{MAX_RETRIES})[/yellow]"
                )

        except ConnectionError:
            if console:
                console.print(
                    f"[yellow]⚠ Connection error loading {movie_title} (attempt {attempt}/{MAX_RETRIES})[/yellow]"
                )

        except HTTPError as e:
            if console:
                console.print(f"[red]✗ HTTP {e.response.status_code} error for {movie_title}[/red]")
            # Don't retry on 4xx client errors
            if e.response.status_code < 500:
                raise

        except RequestException:
            if console:
                console.print(
                    f"[yellow]⚠ Request error loading {movie_title} (attempt {attempt}/{MAX_RETRIES})[/yellow]"
                )

        # Wait before retrying (exponential backoff)
        if attempt < MAX_RETRIES:
            wait_time = RETRY_BACKOFF_FACTOR**attempt
            time.sleep(wait_time)

    # All retries exhausted
    raise RuntimeError(f"Failed to load script: {movie_title}")


def load_and_split_scripts(console: Console, show_progress: bool = False) -> list[Document]:
    """Load and split all Star Wars scripts into chunks.

    Args:
        console: Rich console for displaying progress
        show_progress: Whether to show individual progress bar (default: False)

    Returns:
        List of document chunks
    """
    script_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
        separators=["\nINT.", "\nEXT.", "\n\n", "\n", " ", ""],
    )

    all_chunks = []

    for script in STAR_WARS_SCRIPTS:
        doc = load_star_wars_script(script["url"], script["title"], console)
        chunks = script_splitter.split_documents([doc])
        all_chunks.extend(chunks)

    return all_chunks
