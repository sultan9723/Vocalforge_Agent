import os
import subprocess
import time

START = 10    # starting file number
END = 104     # ending file number
BATCH_SIZE = 10

def run_generate(file_number):
    file_str = str(file_number).zfill(3)
    print(f"\n🎙 Generating voices for input_{file_str}.txt...")
    subprocess.run(["python", "generate_voices.py", file_str], check=True)

def run_merge(file_number):
    file_str = str(file_number).zfill(3)
    print(f"\n🔀 Merging voices for input_{file_str}...")
    subprocess.run(["python", "merge_voices.py", file_str], check=True)

def process_batch(start, end):
    for file_number in range(start, end + 1):
        try:
            run_generate(file_number)
            run_merge(file_number)
            time.sleep(1)  # small delay between files
        except Exception as e:
            print(f"⚠ Error processing input_{str(file_number).zfill(3)}: {e}")
            return False
    return True

current = START
while current <= END:
    batch_end = min(current + BATCH_SIZE - 1, END)
    print(f"\n✅ Processing batch {current} to {batch_end}...")
    
    success = process_batch(current, batch_end)
    if not success:
        print("❌ Stopped due to an error. Fix issue and rerun.")
        break

    current += BATCH_SIZE
    print(f"✅ Completed batch {current - BATCH_SIZE} to {batch_end}. Continuing to next batch...\n")
    time.sleep(2)

print("\n🎉 ALL DONE! All files generated & merged successfully.")