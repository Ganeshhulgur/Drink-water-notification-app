"""
=====================================================================
  💧 WATER DRINKING REMINDER  💧
=====================================================================
A beginner-friendly Python project that reminds you to drink water
every hour with a desktop notification.

This single file is written as a TUTORIAL. It intentionally uses
every core Python concept so you can learn by reading:

  1.  Comments & docstrings
  2.  Variables & data types (int, float, str, bool)
  3.  Strings & f-strings
  4.  Lists
  5.  Dictionaries
  6.  Functions (parameters, return values, default args)
  7.  Conditionals (if / elif / else)
  8.  Loops (for, while)
  9.  Modules (import)
  10. Error handling (try / except / finally)
  11. OOP: class, __init__, self, attributes, methods
  12. OOP: encapsulation, inheritance, polymorphism, @property
  13. The  if __name__ == "__main__"  entry point

Author: You (learning Python!)
=====================================================================
"""

# ---------------------------------------------------------------
# 9. MODULES (import)
# ---------------------------------------------------------------
# "import" pulls in code written by others so we don't reinvent it.
# These three come built-in with Python (no installation needed):
import time         # lets us pause the program (time.sleep)
import random       # lets us pick a random message
from datetime import datetime  # lets us read the current clock time


# ===============================================================
# 2 & 3. VARIABLES, DATA TYPES, STRINGS
# ===============================================================
# A variable is just a name that points to a value.
# Python figures out the TYPE automatically.

APP_NAME = "Water Reminder"      # str  -> text
INTERVAL_SECONDS = 3600          # int  -> whole number (3600 sec = 1 hour)
DAILY_GOAL_LITRES = 2.5          # float-> decimal number
IS_RUNNING = True                # bool -> True / False

# A list = an ORDERED collection you can loop over. Index starts at 0.
REMINDER_MESSAGES = [
    "💧 Time to drink some water!",
    "🚰 Stay hydrated — grab a glass of water!",
    "💦 Your body will thank you. Drink up!",
    "🥤 Hydration break! Take a sip.",
]

# A dictionary = KEY : VALUE pairs. Great for labelled data.
glass_sizes_ml = {
    "small": 150,
    "medium": 250,
    "large": 400,
}


# ===============================================================
# 6. FUNCTIONS
# ===============================================================
# A function is a reusable block of code. "def" defines one.
# It can take PARAMETERS and RETURN a value.

def get_timestamp():
    """Return the current time as a nice string like '06:45 PM'."""
    now = datetime.now()                 # ask the computer for the time
    return now.strftime("%I:%M %p")      # format it (return sends it back)


def pick_message():
    """Pick a random reminder message from the list."""
    return random.choice(REMINDER_MESSAGES)


# Default argument: if you don't pass 'size', it uses "medium".
def glasses_needed(goal_litres=DAILY_GOAL_LITRES, size="medium"):
    """Calculate how many glasses are needed to hit the daily goal."""
    goal_ml = goal_litres * 1000         # convert litres -> millilitres
    one_glass = glass_sizes_ml[size]     # look up the glass size in the dict

    # 7. CONDITIONALS (if / elif / else)
    if one_glass <= 0:
        return 0                         # guard against bad data
    else:
        # round UP so we never under-drink; // is integer division
        return (goal_ml + one_glass - 1) // one_glass


# ===============================================================
# 11 & 12. OBJECT-ORIENTED PROGRAMMING (OOP)
# ===============================================================
# A CLASS is a blueprint. An OBJECT is one thing built from it.
# Think: class = "cookie cutter", object = "the cookie".

class Notifier:
    """
    Base class (parent) that knows how to show a notification.
    Other classes will INHERIT from this one.
    """

    # __init__ is the CONSTRUCTOR. It runs automatically when you
    # create an object. 'self' refers to the specific object.
    def __init__(self, app_name):
        self.app_name = app_name     # 'attribute' stored on the object

    # A METHOD is a function that belongs to a class.
    def notify(self, message):
        """Default behaviour: just print to the screen."""
        print(f"[{self.app_name}] {message}")


class DesktopNotifier(Notifier):
    """
    Child class that INHERITS from Notifier.
    It tries to show a REAL macOS pop-up; if that fails,
    it falls back to the parent's print behaviour.
    This is POLYMORPHISM: same method name 'notify',
    different behaviour.
    """

    def notify(self, message):
        """Override: show a native desktop notification on macOS."""
        # 10. ERROR HANDLING (try / except)
        try:
            import os
            # macOS can show a notification via AppleScript.
            # We escape quotes so the text is safe inside the command.
            safe = message.replace('"', '')
            os.system(
                f'osascript -e \'display notification "{safe}" '
                f'with title "{self.app_name}"\''
            )
            # also print so you see it in the terminal
            print(f"[{self.app_name}] {message}")
        except Exception as error:
            # If anything goes wrong, fall back to the parent method.
            print("Could not show desktop popup, printing instead.")
            super().notify(message)      # super() = call the PARENT version


class WaterTracker:
    """
    Encapsulates (bundles) the DATA + BEHAVIOUR of tracking water.
    Demonstrates encapsulation and @property.
    """

    def __init__(self, goal_litres=DAILY_GOAL_LITRES):
        self.goal_litres = goal_litres
        self._glasses_drunk = 0          # leading _ means "internal use"

    # @property lets a method be accessed like an attribute (no parens).
    @property
    def glasses_drunk(self):
        """Read-only view of how many glasses have been logged."""
        return self._glasses_drunk

    def log_glass(self):
        """Record that one glass of water was drunk."""
        self._glasses_drunk += 1         # same as: x = x + 1

    def summary(self):
        """Return a friendly progress string."""
        target = glasses_needed(self.goal_litres)
        return f"You've logged {self._glasses_drunk} of {target} glasses today."


# ===============================================================
# 13. THE MAIN FUNCTION — the heart of the program
# ===============================================================
def main():
    """Run the reminder loop forever (until you press Ctrl+C)."""

    # Create OBJECTS from our classes:
    notifier = DesktopNotifier(APP_NAME)   # object #1
    tracker = WaterTracker()               # object #2

    print("=" * 50)
    print(f"{APP_NAME} started at {get_timestamp()}")
    print(f"Goal: {DAILY_GOAL_LITRES} litres "
          f"(~{glasses_needed()} medium glasses)")
    print("Press Ctrl+C to stop.")
    print("=" * 50)

    # 8. LOOP (while) — 'while True' repeats forever.
    try:
        while True:
            # Build and send the reminder
            message = pick_message()
            notifier.notify(f"{message}  (at {get_timestamp()})")

            # Pretend the user drinks a glass each reminder:
            tracker.log_glass()
            print(tracker.summary())

            # Wait one hour before the next reminder.
            # (Tip: while testing, change INTERVAL_SECONDS to 5.)
            print(f"Next reminder in {INTERVAL_SECONDS // 60} minutes...\n")
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        # Runs when you press Ctrl+C — a clean way to exit.
        print("\nStopping Water Reminder. Stay hydrated! 👋")

    finally:
        # 'finally' ALWAYS runs — good for cleanup / final messages.
        print(tracker.summary())


# ---------------------------------------------------------------
# This special line means: "only run main() if this file is run
# directly, not when it is imported by another file."
# ---------------------------------------------------------------
if __name__ == "__main__":
    main()

