"""
🎙 Accent Selector Module

This script allows users to select a regional accent based on their selected language.
If no accents are available for the language, it falls back to the original language code.
"""

def get_accent(language_code):
    accents_by_language = {
        "en": ["en-US", "en-GB", "en-IN", "en-AU", "en-IE", "en-NZ"],
        "es": ["es-ES", "es-MX", "es-US"],
        "fr": ["fr-FR", "fr-CA"],
        "de": ["de-DE"],
        "it": ["it-IT"],
        "pt": ["pt-PT", "pt-BR"],
        "ar": ["ar-SA", "ar-EG", "ar-AE"],
        "hi": ["hi-IN"],
        "bn": ["bn-IN", "bn-BD"],
        "zh": ["zh-CN", "zh-TW", "zh-HK"],
        "ja": ["ja-JP"],
        "ko": ["ko-KR"],
        "ru": ["ru-RU"],
        "tr": ["tr-TR"],
        "id": ["id-ID"],
        "th": ["th-TH"],
        "vi": ["vi-VN"],
        "pl": ["pl-PL"],
        "nl": ["nl-NL"],
        "sv": ["sv-SE"],
        "fi": ["fi-FI"],
        "no": ["no-NO"],
        "da": ["da-DK"]
    }

    base_lang = language_code[:2]
    available_accents = accents_by_language.get(base_lang, [language_code])

    print(f"\n🌍 Available accents for '{language_code}':")
    for i, acc in enumerate(available_accents, 1):
        print(f"{i}. {acc}")

    choice = input("Select an accent number [default 1]: ").strip()
    try:
        return available_accents[int(choice) - 1]
    except (IndexError, ValueError):
        return available_accents[0]