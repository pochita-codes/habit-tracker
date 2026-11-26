# logger.py
# CLI flow for entering today's habit data.

from datetime import date
from rich.console import Console
from rich.prompt import Prompt

from config import get_active_habits
import storage

console = Console()


def _ask_bool_or_skip(name):
    """Ask a yes/no question, allowing 'skip' as a third option.
    Returns True, False, or None (meaning: skipped)."""
    answer = Prompt.ask(
        f"[cyan]{name}[/cyan]?",
        choices=["y", "n", "skip"],
    )
    if answer == "skip":
        return None
    return answer == "y"


def _ask_numeric_or_skip(name, unit):
    """Ask for a numeric value, allowing 'skip'. Retries on invalid
    (non-numeric, non-skip) input -- mimics what FloatPrompt did
    automatically, since we can't use FloatPrompt anymore (it has no
    concept of 'skip')."""
    while True:
        raw = Prompt.ask(f"[cyan]{name}[/cyan]? (in {unit} or 'skip')")
        if raw.strip().lower() == "skip":
            return None 
        try:
            return float(raw)
        except ValueError:
            console.print("[red]Not a valid number — try again.[/red]")


def log_today():
    """Walk through each active habit and prompt for today's value.
    Typing 'skip' leaves that habit unlogged for today instead of
    forcing a value."""
    today = date.today()
    console.print(f"\n[bold]Logging habits for {today}[/bold]\n")

    for habit in get_active_habits():
        name = habit["name"]

        if habit["type"] == "bool":
            value = _ask_bool_or_skip(name)
        else:  # numeric
            unit = habit["unit"] or ""
            value = _ask_numeric_or_skip(name, unit)

        if value is None:
            console.print(f"  [yellow]skipped[/yellow] {name}\n")
            continue

        storage.log_entry(today, name, value)
        console.print(f"  [green]✓[/green] Logged {name}: {value}\n")

    console.print("All habits logged for today.\n")


if __name__ == "__main__":
    log_today()