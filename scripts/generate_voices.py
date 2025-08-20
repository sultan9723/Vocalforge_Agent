import os
import sys
import re
from gtts import gTTS
from xml.sax.saxutils import escape
import requests
import random
from dotenv import load_dotenv
load_dotenv()
# === Azure Keys & Region ===
azure_key = os.getenv("AZURE_API_KEY")
region = os.getenv("AZURE_REGION")
endpoint = os.getenv("AZURE_ENDPOINT")


# Voices: Male 1 → Female → Male 2
azure_voices = ["en-US-GuyNeural", "en-US-JennyNeural", "en-US-DavisNeural"]
gtts_accents = ["com", "co.uk", "com.au"]  # fallback accents

current_key_index = 0
MAX_WORDS = 530       # ~3:35 min max
MIN_WORDS = 350       # ~2:30 min min
FILLERS = [
    "That’s actually a really good point.",
    "I think that makes a lot of sense.",
    "Yeah, that’s true when you think about it.",
    "I feel like we can definitely agree on that."
]

def get_azure_key():
    global current_key_index
    if current_key_index >= len(AZURE_KEYS):
        return None
    return AZURE_KEYS[current_key_index]

def switch_key():
    global current_key_index
    current_key_index += 1
    if current_key_index >= len(AZURE_KEYS):
        print("❌ All Azure keys exhausted! Switching permanently to gTTS fallback.")

# === File Selection ===
input_number = sys.argv[1] if len(sys.argv) > 1 else "001"
input_file = f"inputs/input_{input_number}.txt"
print(f"\n📄 Processing file: {input_file}")

# === Read & Clean Text ===
try:
    with open(input_file, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()
except FileNotFoundError:
    raise FileNotFoundError(f"❌ File not found: {input_file}")
except UnicodeDecodeError:
    raise ValueError("❌ Could not decode input file. Save in UTF-8 format.")

def clean_line(line):
    line = line.strip()
    line = re.sub(r"^(Title|Speaker 1|Speaker 2|Speaker 3|Closing Line):", "", line, flags=re.IGNORECASE).strip()
    line = re.sub(r"\[.*?\]", "", line)
    line = re.sub(r"\(.*?\)", "", line)
    return line

cleaned_lines = list(filter(None, [clean_line(line) for line in raw_lines]))

if len(cleaned_lines) < 4:
    raise ValueError("⚠ File must have at least 3 paragraphs for 3 speakers!")

title = escape(cleaned_lines[0])
speaker_paragraphs = cleaned_lines[1:4]

# === Duration Adjustment ===
def adjust_length(text):
    words = text.split()
    if len(words) > MAX_WORDS:
        words = words[:MAX_WORDS]
    elif len(words) < MIN_WORDS:
        while len(words) < MIN_WORDS:
            words += random.choice(FILLERS).split()
    return " ".join(words)

def format_text_with_pauses(text):
    text = escape(text)
    text = re.sub(r"\.\s*", ".<break time='600ms'/> ", text)
    text = re.sub(r",\s*", ",<break time='300ms'/> ", text)
    return text

speaker_texts = []
for i, paragraph in enumerate(speaker_paragraphs):
    paragraph = adjust_length(paragraph)
    paragraph = format_text_with_pauses(paragraph)
    rate = "medium"
    if i == 0:
        text = f"<prosody rate='{rate}'>{title}.<break time='700ms'/> {paragraph}</prosody>"
    else:
        text = f"<break time='900ms'/><prosody rate='{rate}'>{paragraph}</prosody>"
    speaker_texts.append(text)

os.makedirs("output", exist_ok=True)

# === Generate Voices ===
for i, text in enumerate(speaker_texts):
    output_path = f"output/speaker{i+1}_{input_number}.mp3"
    print(f"\n🎙 Generating Speaker {i+1} voice...")

    azure_available = True
    while azure_available:
        key = get_azure_key()
        if not key:
            azure_available = False
            break

        ssml = f"""<speak version='1.0' xml:lang='en-US'>
        <voice name='{azure_voices[i]}'>{text}</voice>
        </speak>"""

        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "PythonTTSApp"
        }

        try:
            response = requests.post(AZURE_ENDPOINT, headers=headers, data=ssml.encode('utf-8'))
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Saved: {output_path}")
                azure_available = False
            elif response.status_code in [429, 403]:
                print("⚠ Azure quota exceeded! Switching key...")
                switch_key()
            else:
                print(f"❌ Azure TTS Error {response.status_code}: {response.text}")
                azure_available = False
        except:
            azure_available = False

    # === gTTS fallback if Azure unavailable ===
    if not os.path.exists(output_path):
        try:
            print(f"⚠ Using gTTS fallback for Speaker {i+1}...")
            tts = gTTS(text=adjust_length(speaker_paragraphs[i]), lang="en", tld=gtts_accents[i])
            tts.save(output_path)
            print(f"✅ gTTS fallback saved: {output_path}")
        except Exception as e:
            print(f"❌ gTTS failed for Speaker {i+1}: {e}")

print("\n🎉 All done! Voices saved in /output folder.")