import os
import time
import re
import requests
from dotenv import load_dotenv
load_dotenv()
# === Config ===
gemini_key = os.getenv("GEMINI_API_KEY")
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
HEADERS = {"Content-Type": "application/json"}
INPUT_DIR = "inputs"
TARGET_WORD_COUNT = 480

# === Utils ===
def count_words(text):
    return len(re.findall(r'\w+', text))

def remove_extra_blank_lines(text):
    return re.sub(r'\n\s*\n+', '\n', text.strip())

def read_input_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_output_file(filepath, content):
    cleaned = remove_extra_blank_lines(content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned)

def call_gemini(prompt, api_key):
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(f"{ENDPOINT}?key={api_key}", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# === Prompt Builder ===
def build_prompt(existing_text, target_count):
    return f"""
The following is a script of an academic-style voice discussion among three students. Your task is to keep the *exact format* (title, Speaker 1, Speaker 2, Speaker 3, and the closing line), but expand ONLY the speaker paragraphs so that the final script reaches around {target_count} words in total — not more.

❗ Do NOT change the title, pauses, introduction, or closing line.
✅ Just extend each speaker's paragraph in a natural, academic tone.
⛔ No empty lines or format changes.

Here is the original script:
---
{existing_text}
---
Now return the updated version with expanded speaker sections only. Preserve formatting exactly. Avoid over-expanding.
"""

# === Expansion Logic ===
def expand_short_file(filepath):
    content = read_input_file(filepath)
    original_words = count_words(content)

    if original_words >= TARGET_WORD_COUNT:
        print(f"[✓] Already long enough: {filepath}")
        return

    print(f"[→] Expanding: {filepath} ({original_words} words)")
    prompt = build_prompt(content, TARGET_WORD_COUNT)

    for key_index, api_key in enumerate(API_KEYS):
        try:
            expanded_text = call_gemini(prompt, api_key)
            if count_words(expanded_text) >= TARGET_WORD_COUNT:
                write_output_file(filepath, expanded_text)
                print(f"[✓] Expanded and saved: {filepath} using API Key #{key_index + 1}")
                return
            else:
                print(f"[⚠] Expansion not enough with API Key #{key_index + 1}, trying next...")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"[⚠] Rate limit hit on API Key #{key_index + 1}. Trying next...")
                time.sleep(3)
                continue
            else:
                print(f"[✗] HTTP error on {filepath} with API Key #{key_index + 1}: {e}")
                break
        except Exception as e:
            print(f"[✗] Unexpected error on {filepath} with API Key #{key_index + 1}: {e}")
            break

    print(f"[!] Skipped {filepath} — All keys failed or expansion too weak.")

# === Main ===
def main():
    print("🔍 Expanding only files listed in needs_expansion.txt...")

    if not os.path.exists("needs_expansion.txt"):
        print("❌ needs_expansion.txt not found.")
        return

    with open("needs_expansion.txt", "r", encoding="utf-8") as f:
        file_list = [line.strip() for line in f if line.strip()]

    for filename in file_list:
        filepath = os.path.join(INPUT_DIR, filename)

        if not os.path.exists(filepath):
            print(f"[!] Missing: {filename}")
            continue

        expand_short_file(filepath)
        time.sleep(1.5)

    print("✅ Done expanding selected short files.")

if __name__== "__main__":
    main()