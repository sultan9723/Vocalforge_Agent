import os
import openai
import time

# Set your OpenAI API key
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Ensure input folder exists
os.makedirs("inputs", exist_ok=True)

# Load topics
with open("topics.txt", "r", encoding="utf-8") as f:
    topics = [line.strip() for line in f if line.strip()]

# Set limits
total_files = 500
max_retries = 3

# Duration strategy
durations = (
    [150] * 200 +  # 2:30 mins
    [180] * 200 +  # 3:00 mins
    [195] * 100    # 3:15 mins
)

for i in range(total_files):
    topic = topics[i % len(topics)]
    est_duration = durations[i]

    file_index = str(i + 1).zfill(3)
    output_path = f"inputs/input_{file_index}.txt"

    # Prompt to ensure all speakers discuss the same topic
    prompt = f"""You are writing a 3-person academic group discussion.
Each speaker must speak clearly on the same topic in a natural discussion style.
Ensure:
- Speaker 1 speaks the title first and then discusses.
- Speaker 2 and Speaker 3 respond with unique academic input on the *same topic*.
- The tone is formal, academic, and realistic.
- Total speaking time is {est_duration} seconds total ({round(est_duration/3)}s per speaker).

Topic: {topic}

Format:
Speaker 1:
Title: {topic}
[short pause]
[Speaker 1's statement]

Speaker 2:
[Speaker 2's opinion]

Speaker 3:
[Speaker 3's thoughts]
"""

    success = False
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an academic discussion writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            discussion = response.choices[0].message.content.strip()

            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(discussion)

            print(f"✅ Created: {output_path}")
            success = True
            break
        except Exception as e:
            print(f"❌ Error for input_{file_index}.txt (Attempt {attempt + 1}): {e}")
            time.sleep(2)

    if not success:
        print(f"⚠ Failed to create: input_{file_index}.txt after {max_retries} attempts")