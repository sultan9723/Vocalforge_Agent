# scripts/ai_agent.py

import os
import subprocess
import time

# ------------------ CONFIG ------------------
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPTS_DIR, "../inputs")
OUTPUT_DIR = os.path.join(SCRIPTS_DIR, "../output")
TEMP_DIR = os.path.join(SCRIPTS_DIR, "../temp")

SELECTION_SCRIPTS = [
    "select_gender.py",
    "select_language.py",
    "select_duration.py",
    "select_accent.py",
    "select_age.py"
]

GENERATION_SCRIPT = "generate_all_stepwise.py"
MERGE_SCRIPT = "merge_all.py"

# ------------------ UTILITY ------------------
def run_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print(f"\n▶ Running: {script_name}")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Error in {script_name}:")
        print(result.stderr)
    else:
        print(f"✅ Done: {script_name}")
        print(result.stdout)

# ------------------ AGENT START ------------------
def main():
    print("\n🎙 Welcome to the AI Voice Generation Agent")
    print("⚙  Initializing environment...\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Step 1: Collect Profile Preferences
    for script in SELECTION_SCRIPTS:
        run_script(script)

    # Step 2: Generate Voices Step-by-Step
    run_script(GENERATION_SCRIPT)

    # Step 3: Merge All Voices
    run_script(MERGE_SCRIPT)

    print("\n🚀 All tasks completed. Final voices are in the 'output' folder.")
    print("🧠 Smart AI Agent execution finished.\n")

if __name__ == "__main__":
    start_time = time.time()
    try:
        main()
    except Exception as e:
        print(f"🔥 Agent crashed: {e}")
    finally:
        duration = time.time() - start_time
        print(f"⏱ Execution time: {round(duration, 2)} seconds")