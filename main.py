# main.py
# Entry point -- orchestrates logger.py and grid.py through an interactive menu.

from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt

import logger
import grid

console = Console()


def _prompt_week_date():
    """Ask for any date within the target week (mm/dd/yyyy). Retries on
    bad format instead of crashing."""
    while True:
        raw = Prompt.ask("Enter a date in that week (mm/dd/yyyy)")
        try:
            return datetime.strptime(raw, "%m/%d/%Y").date()
        except ValueError:
            console.print("[red]Invalid format -- please use mm/dd/yyyy (e.g. 08/05/2026)[/red]")


def _prompt_month_date():
    """Ask for a month (mm/yyyy), return a date set to the 1st of that month."""
    while True:
        raw = Prompt.ask("Enter the month (mm/yyyy)")
        try:
            parsed = datetime.strptime(raw, "%m/%Y")
            return parsed.date().replace(day=1)
        except ValueError:
            console.print("[red]Invalid format -- please use mm/yyyy (e.g. 08/2026)[/red]")


def view_progress():
    """Ask week or month, prompt for the relevant date, then render the grid."""
    view = Prompt.ask("View by [cyan]week[/cyan] or [cyan]month[/cyan]?", choices=["week", "month"])

    if view == "week":
        reference_date = _prompt_week_date()
    else:
        reference_date = _prompt_month_date()

    grid.show_grid(view, reference_date)


def main_menu():
    while True:
        console.print("\nHabit tracker")
        choice = Prompt.ask(
            r"\[[cyan]l[/cyan]]og today, \[[cyan]v[/cyan]]iew progress, or \[[cyan]q[/cyan]]uit?",
            choices=["l", "v", "q"],
        )

        if choice == "l":
            logger.log_today()
        elif choice == "v":
            view_progress()
        else:
            console.print("🫡\n")
            break


if __name__ == "__main__":
    main_menu()