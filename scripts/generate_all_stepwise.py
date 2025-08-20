import os
import subprocess
import sys

INPUT_DIR = "inputs"
TOTAL_FILES = 500

print("🎙 Starting step-by-step voice generation...")

for i in range(1, TOTAL_FILES + 1):
    file_number = str(i).zfill(3)
    input_file = os.path.join(INPUT_DIR, f"input_{file_number}.txt")

    if not os.path.exists(input_file):
        print(f"[!] Skipping missing file: {input_file}")
        continue

    print(f"\n[{file_number}] Generating voice for: {input_file}")
    try:
        subprocess.run([sys.executable, "generate_voices.py", file_number], check=True)
        print(f"✅ Completed: input_{file_number}.txt")

    except subprocess.CalledProcessError as e:
        print(f"[❌] Error processing input_{file_number}.txt: {e}")
        proceed = input("Do you want to continue with the next file? (Y/N): ").strip().lower()
        if proceed != "y":
            print("⏹ Stopping as per your request.")
            break

    # ✅ Ask before moving to the next file
    proceed = input("Do you want to process the next file? (Y/N): ").strip().lower()
    if proceed != "y":
        print("⏹ Stopping step-by-step generation.")
        break

print("\n🎉 Step-by-step generation finished.")