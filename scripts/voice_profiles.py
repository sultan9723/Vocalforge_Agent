# voice_profiles.py

# Base list of some pre-configured voices for quick access
BASE_VOICES = [
    {
        "id": "1",
        "name": "English - Female (US) - Young Adult",
        "language": "en-US",
        "voice": "en-US-AriaNeural",
        "gender": "Female",
        "age": "YoungAdult"
    },
    {
        "id": "2",
        "name": "English - Male (UK) - Young Adult",
        "language": "en-GB",
        "voice": "en-GB-RyanNeural",
        "gender": "Male",
        "age": "YoungAdult"
    },
    # ... other key English voices ...
]

# Extended list for broader coverage (abbreviated for clarity)
EXTENDED_VOICES = [
    {"code": "hi-IN", "voice": "hi-IN-SwaraNeural", "name": "Hindi", "gender": "Female"},
    {"code": "ur-PK", "voice": "ur-PK-AsadNeural", "name": "Urdu", "gender": "Male"},
    {"code": "es-MX", "voice": "es-MX-DaliaNeural", "name": "Spanish (MX)", "gender": "Female"},
    {"code": "de-DE", "voice": "de-DE-KatjaNeural", "name": "German", "gender": "Female"},
    {"code": "fr-FR", "voice": "fr-FR-HenriNeural", "name": "French", "gender": "Male"},
    # Expand to 140+ by adding more supported Azure voices...
]

def generate_voice_profiles():
    profiles = {v["id"]: v for v in BASE_VOICES}
    next_id = len(profiles) + 1
    for ext in EXTENDED_VOICES:
        profiles[str(next_id)] = {
            "name": f'{ext["name"]} - Default Voice',
            "language": ext["code"],
            "voice": ext["voice"],
            "gender": ext.get("gender", "NotSpecified"),
            "age": "Default"
        }
        next_id += 1
    return profiles

VOICE_PROFILES = generate_voice_profiles()

if __name__== "__main__":
    # Prints out all voices—useful for debugging or updating
    for vid, info in VOICE_PROFILES.items():
        print(f'{vid}: {info["name"]} ({info["language"]})')