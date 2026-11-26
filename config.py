# config.py
# Defines the habits being tracked and where the data lives.

from pathlib import Path

# Where the Excel log file lives. Path() keeps this OS-independent 
# (works the same on your Mac as it would on Windows/Linux).
DATA_FILE = Path("habit_log.xlsx")

# Each habit is a dictionary describing how it should be tracked and displayed.
# - name: the label used everywhere (CLI prompts, Excel sheet, grid headers)
# - type: "bool" for yes/no habits, "numeric" for habits that need a number
# - target: minimum value needed to count as "done" (numeric only, None for bool)
# - unit: label shown next to the number when logging (numeric only, None for bool)
# - active: whether this habit is currently being logged/displayed
HABITS = [
    {"name": "gym",       "type": "bool",    "target": None, "unit": None,    "active": True}
    ,{"name": "meal plan", "type": "bool",    "target": None, "unit": None,    "active": True}
    ,{"name": "sleep",     "type": "numeric", "target": 7,    "unit": "hours", "active": True}
    ,{"name": "to-do", "type": "bool", "target": None, "unit": None, "active": True}
    ,{"name": "journal", "type": "bool", "target": None, "unit": None, "active": True}
    ,{"name": "no-goon", "type": "bool", "target": None, "unit": None, "active": True}
]


def get_active_habits():
    """Return only the habits currently being tracked (skips inactive ones)."""
    return [habit for habit in HABITS if habit["active"]]


def get_habit(name):
    """Look up a single habit's definition by name. Returns None if not found."""
    for habit in HABITS:
        if habit["name"] == name:
            return habit
    return None