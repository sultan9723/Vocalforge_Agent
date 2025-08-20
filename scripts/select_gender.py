# select_gender_accent.py

def select_voice_gender_age():
    options = {
        "1": "male_adult",
        "2": "female_adult",
        "3": "male_child",
        "4": "female_child",
        "5": "male_senior",
        "6": "female_senior"
    }

    print("\n🗣 Choose voice type:")
    print("1. Male Adult")
    print("2. Female Adult")
    print("3. Male Child")
    print("4. Female Child")
    print("5. Male Senior")
    print("6. Female Senior")

    while True:
        choice = input("Enter your choice (1–6): ").strip()
        if choice in options:
            return options[choice]
        else:
            print("❌ Invalid choice. Try again.")

def select_accent_by_language(language_code):
    # Default: if not language-specific accents are available, return neutral
    accents = {
        "en-US": ["Standard", "Southern", "African-American", "Valley Girl", "New Yorker"],
        "en-UK": ["Standard", "British RP", "Liverpool", "Scottish", "Welsh", "Cockney"],
        "hi-IN": ["Standard", "North Indian", "South Indian"],
        "es-ES": ["Standard", "Latin American", "Castilian"],
        "fr-FR": ["Standard", "Belgian", "Canadian"],
        "de-DE": ["Standard", "Austrian", "Swiss German"],
        # Add more accents as needed
    }

    available_accents = accents.get(language_code, ["Standard"])

    print(f"\n🎭 Available accents for {language_code}:")
    for i, accent in enumerate(available_accents):
        print(f"{i + 1}. {accent}")

    while True:
        try:
            index = int(input("Select accent number: "))
            if 1 <= index <= len(available_accents):
                return available_accents[index - 1]
            else:
                print("Invalid number.")
        except ValueError:
            print("Enter a valid number.")