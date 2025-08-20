from voice_profiles import VOICE_PROFILES

def list_voice_options():
    print("\n🗣 Available Voices:\n")
    for vid, v in VOICE_PROFILES.items():
        print(f"[{vid}] {v['name']} | Language: {v['language']} | Gender: {v['gender']} | Age: {v['age']}")

def get_voice_by_id(voice_id):
    return VOICE_PROFILES.get(voice_id)

def choose_multiple_voices(n=3):
    selected = []
    list_voice_options()
    for i in range(n):
        while True:
            vid = input(f"\n➡ Enter Voice ID for Speaker {i+1}: ").strip()
            voice = get_voice_by_id(vid)
            if voice:
                selected.append(voice)
                break
            else:
                print("❌ Invalid ID. Try again.")
    return selected