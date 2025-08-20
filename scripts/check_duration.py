import os

INPUT_FOLDER = "inputs"  # change if needed
WORDS_PER_SECOND = 2.5

def check_files():
    print(f"🔍 Looking for files in: {os.path.abspath(INPUT_FOLDER)}")
    
    if not os.path.exists(INPUT_FOLDER):
        print("❌ Folder not found!")
        return

    files = os.listdir(INPUT_FOLDER)
    print(f"📂 Found files: {files}")

    found_txt = False
    for file_name in files:
        if file_name.endswith(".txt"):
            found_txt = True
            file_path = os.path.join(INPUT_FOLDER, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            word_count = len(text.split())
            duration_sec = word_count / WORDS_PER_SECOND
            minutes = int(duration_sec // 60)
            seconds = int(duration_sec % 60)

            print(f"✅ {file_name} — {word_count} words ≈ {minutes}:{seconds:02d} min")

    if not found_txt:
        print("⚠ No .txt files found in this folder!")


    if __name__== "_main__":
        check_files()