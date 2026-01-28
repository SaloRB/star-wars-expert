"""UI components for Star Wars Expert."""

import threading
import time

from rich.console import Console
from rich.live import Live
from rich.panel import Panel

from config import SPINNER_FRAMES


def create_step_display(
    steps: list[tuple[str, str]], spinner_frame: int = 0, title: str = "Progress"
) -> Panel:
    """Create a panel showing progress steps.

    Args:
        steps: List of (description, status) tuples. Status can be "done", "running", or "pending".
        spinner_frame: Current frame index for spinner animation.
        title: Panel title.

    Returns:
        Rich Panel with formatted step display.
    """
    lines = []
    for i, (desc, status) in enumerate(steps):
        if status == "done":
            marker = "[green]✓[/green]"
        elif status == "running":
            marker = f"[cyan]{SPINNER_FRAMES[spinner_frame % len(SPINNER_FRAMES)]}[/cyan]"
        else:  # pending
            marker = "[dim]○[/dim]"

        step_num = f"[dim][{i + 1}/{len(steps)}][/dim]"
        lines.append(f"   {step_num} {desc:<30} {marker}")

    content = "\n".join(lines)
    return Panel(content, title=f"[bold cyan]{title}[/bold cyan]", border_style="cyan")


class StepProgress:
    """Manages step-by-step progress with animated spinner.

    Example:
        progress = StepProgress(console, ["Step 1", "Step 2", "Step 3"])
        progress.start()
        progress.advance()  # Start step 1
        # ... do work ...
        progress.advance()  # Complete step 1, start step 2
        # ... do work ...
        progress.complete("Done!")
    """

    def __init__(
        self, console: Console, steps: list[str], title: str = "🚀 Initializing Star Wars Expert"
    ):
        """Initialize step progress.

        Args:
            console: Rich console for display.
            steps: List of step descriptions.
            title: Panel title.
        """
        self.console = console
        self.title = title
        self.steps = [(s, "pending") for s in steps]
        self.current_step = -1
        self.spinner_frame = 0
        self.running = False
        self.live = None
        self._spinner_thread = None

    def start(self):
        """Start the progress display with animated spinner."""
        self.live = Live(
            create_step_display(self.steps, title=self.title),
            console=self.console,
            refresh_per_second=10,
        )
        self.live.start()
        self.running = True
        self._spinner_thread = threading.Thread(target=self._animate_spinner, daemon=True)
        self._spinner_thread.start()

    def _animate_spinner(self):
        """Animate the spinner in background thread."""
        while self.running:
            time.sleep(0.1)
            self.spinner_frame += 1
            if self.live:
                self.live.update(create_step_display(self.steps, self.spinner_frame, self.title))

    def advance(self):
        """Mark current step as done and move to next step."""
        if self.current_step >= 0:
            desc = self.steps[self.current_step][0]
            self.steps[self.current_step] = (desc, "done")

        self.current_step += 1
        if self.current_step < len(self.steps):
            desc = self.steps[self.current_step][0]
            self.steps[self.current_step] = (desc, "running")

        if self.live:
            self.live.update(create_step_display(self.steps, self.spinner_frame, self.title))

    def complete(self, message: str = ""):
        """Complete all steps and stop the display.

        Args:
            message: Optional completion message to display.
        """
        # Mark all remaining as done
        for i in range(len(self.steps)):
            desc = self.steps[i][0]
            self.steps[i] = (desc, "done")

        self.running = False
        if self.live:
            self.live.update(create_step_display(self.steps, self.spinner_frame, self.title))
            self.live.stop()

        if message:
            self.console.print(message)
