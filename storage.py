# storage.py
# Reads and writes daily habit entries to the Excel log file.
# Each row represents one (date, habit) entry: Date | Habit | Value

from datetime import datetime, date
from openpyxl import Workbook, load_workbook
from config import DATA_FILE

HEADERS = ["Date", "Habit", "Value"]

# Helper function to deal with different date formats
def _normalize_date(value):
    """
    openpyxl sometimes returns dates as datetime objects -- strip the time component
    so all date comaprisons/storage use plain date objects and not datetime
    """
    if isinstance(value, datetime):
        return value.date()
    return value

def _load_or_create_workbook():
    """Open the Excel file if it exists, otherwise create one with headers.
    Leading underscore signals this is an internal helper -- other files
    shouldn't call it directly, they should go through log_entry/get_all_entries."""
    if DATA_FILE.exists():
        return load_workbook(DATA_FILE)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Log"
    sheet.append(HEADERS)
    workbook.save(DATA_FILE)
    return workbook


def log_entry(entry_date, habit_name, value):
    """
    Write one habit entry for a given date.
    If an entry already exists for that (date, habit) pair, overwrite it
    instead of adding a duplicate row -- so re-logging the same day corrects
    the value rather than leaving two conflicting rows behind.
    """
    workbook = _load_or_create_workbook()
    sheet = workbook["Log"]

    # min_row=2 skips the header row. Each `row` here is a tuple of Cell
    # rows are objects (not raw values), which is why we access .value on them.
    for row in sheet.iter_rows(min_row=2):
        # "_" because we access the Value cell via row[2] below instead of by name
        row_date, row_habit, _ = row
        if _normalize_date(row_date.value) == entry_date and row_habit.value == habit_name:
            row[2].value = value  # update the Value cell in place
            workbook.save(DATA_FILE)
            return

   # for row in sheet.iter_rows(min_row=2):
   #  row_date, row_habit, row_value = row
   #  if _normalize_date(row_date.value) == entry_date and row_habit.value == habit_name:
   #      row_value.value = value
   #      workbook.save(DATA_FILE)
   #      return

    # No existing entry for this date+habit -- add a new row.
    sheet.append([entry_date, habit_name, value])
    workbook.save(DATA_FILE)


def get_all_entries():
    """
    Read every entry from the log and return it as a list of dicts:
    [{"date": ..., "habit": ..., "value": ...}, ...]
    Returns raw data only -- filtering by week/month or by active habit
    happens elsewhere, not here.
    """
    if not DATA_FILE.exists():
        return []

    workbook = load_workbook(DATA_FILE)
    sheet = workbook["Log"]

    # values_only=True here (unlike log_entry above) because we just want
    # plain Python values back, not Cell objects -- we're not editing anything.
    entries = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        entry_date, habit_name, value = row
        if entry_date is None:
            continue  # skip blank trailing rows, if any
        entries.append({"date": _normalize_date(entry_date), "habit": habit_name, "value": value})
    return entries