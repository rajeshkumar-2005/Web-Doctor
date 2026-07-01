import schedule
import time
from scanner import run_scan
from db import save_scan, get_history

# Change this later to real govt sites
WATCH_URL = "https://google.com"

def job():
    print("Running scheduled scan...")

    # Get last score
    history = get_history()
    old_score = history[0][1] if history else None

    # New scan
    result = run_scan(WATCH_URL)
    new_score = result["risk"]["score"]

    save_scan(WATCH_URL, new_score, result["risk"]["risk"], result)

    print(f"New Score: {new_score}")

    # Compare scores
    if old_score and new_score < old_score:
        print("⚠️ ALERT: Security score dropped!")

# Run every 1 minute (for testing)
schedule.every(1).minutes.do(job)

print("Agent running...")

# First run immediately
job()

while True:
    schedule.run_pending()
    time.sleep(1)