"""
Purpose-
- Turning stored entries into colored square display
- "Done" i.e. colored is defined by what "done" logic means (logger + config + storage)
- Does not impact Excel file 
"""
# grid.py
# Renders each habit's progress as a row of colored squares (done/blank),
# with weekly or monthly views.

# Imports
from datetime import date, timedelta
import calendar

from rich.console import Console
from rich.text import Text

from config import get_active_habits
import storage

# Python's object for stylized printing
# The normal prints raw text, wouldn't print colored squares
console = Console()

FILLED = "■"
BLANK = "□"
DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
COLUMN_WIDTH = 4   # fixed width per day column, so squares and labels line up
LABEL_WIDTH = 12   # width reserved for the habit name column


def _get_week_dates(reference_date=None):
    """Return the 7 dates (Mon-Sun) for the week containing reference_date."""
    reference_date = reference_date or date.today()
    start = reference_date - timedelta(days=reference_date.weekday())
    return [start + timedelta(days=i) for i in range(7)]


def _get_month_dates(reference_date=None):
    """Return every date in the month containing reference_date."""
    reference_date = reference_date or date.today()
    _, days_in_month = calendar.monthrange(reference_date.year, reference_date.month)
    return [date(reference_date.year, reference_date.month, day) for day in range(1, days_in_month + 1)]


def _get_month_weeks(reference_date=None):
    """Return the month as a list of weeks, each week a list of 7 slots
    (Mon-Sun). Days outside the month (padding before day 1 or after the
    last day) are None, so every week row is always exactly 7 wide."""
    reference_date = reference_date or date.today()
    days = _get_month_dates(reference_date)

    weeks = []
    current_week = [None] * days[0].weekday()  # pad before the 1st

    for d in days:
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []

    if current_week:
        current_week += [None] * (7 - len(current_week))  # pad after the last day
        weeks.append(current_week)

    return weeks


def _build_lookup(entries):
    """Turn the flat entries list into a dict keyed by (date, habit_name)."""
    return {(entry["date"], entry["habit"]): entry["value"] for entry in entries}


def _is_done(habit, value):
    """bool habits use the value directly; numeric habits need value >= target."""
    if value is None:
        return False
    if habit["type"] == "bool":
        return bool(value)
    return value >= habit["target"]


def _square_for(habit, d, lookup):
    """Return (symbol, style) for one day's square, or a blank space if
    the date is None (padding outside the month)."""
    if d is None:
        return " " * COLUMN_WIDTH, None
    value = lookup.get((d, habit["name"]))
    done = _is_done(habit, value)
    symbol = FILLED if done else BLANK
    style = "green" if done else "grey50"
    return f"{symbol:<{COLUMN_WIDTH}}", style


def _render_day_header():
    """One row of day-of-week labels, aligned to the same columns as squares."""
    header = Text()
    for label in DAY_LABELS:
        header.append(f"{label:<{COLUMN_WIDTH}}", style="dim bold")
    return header


def _render_habit_row(habit, dates, lookup):
    """Single row of squares for a habit across a flat list of dates (week view)."""
    row = Text()
    for d in dates:
        text, style = _square_for(habit, d, lookup)
        row.append(text, style=style)
    return row


def _render_month_rows(habit, weeks, lookup):
    """Multiple rows of squares for a habit — one row per week in the month."""
    rows = []
    for week in weeks:
        row = Text()
        for d in week:
            text, style = _square_for(habit, d, lookup)
            row.append(text, style=style)
        rows.append(row)
    return rows


def show_grid(view="week", reference_date=None):
    """Print every active habit's grid for the given week or month.
    reference_date can be any date within the target week/month --
    defaults to today if not provided."""
    entries = storage.get_all_entries()
    lookup = _build_lookup(entries)
    habits = get_active_habits()

    if view == "week":
        dates = _get_week_dates(reference_date)
        console.print(f"\n[bold]Week of {dates[0]}[/bold]\n")
        console.print(" " * LABEL_WIDTH, end="")
        console.print(_render_day_header())

        for habit in habits:
            console.print(f"{habit['name']:<{LABEL_WIDTH}}", end="")
            console.print(_render_habit_row(habit, dates, lookup))

    else:  # month
        weeks = _get_month_weeks(reference_date)
        label_date = reference_date or date.today()
        console.print(f"\n[bold]{label_date.strftime('%B %Y')}[/bold]\n")
        console.print(" " * LABEL_WIDTH, end="")
        console.print(_render_day_header())

        for habit in habits:
            console.print(f"[bold]{habit['name']}[/bold]")
            for week_row in _render_month_rows(habit, weeks, lookup):
                console.print(" " * LABEL_WIDTH, end="")
                console.print(week_row)
            console.print()

    console.print()


if __name__ == "__main__":
    show_grid("week")