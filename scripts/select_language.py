# select_language.py

def select_language():
    languages = [
        "en-US", "en-UK", "es-ES", "fr-FR", "de-DE", "hi-IN", "ar-SA", "zh-CN", "ru-RU",
        "ja-JP", "ko-KR", "it-IT", "pt-PT", "tr-TR", "ur-PK", "th-TH", "vi-VN", "fa-IR",
        "nl-NL", "pl-PL", "id-ID", "ms-MY", "bn-BD", "sv-SE", "fi-FI", "no-NO", "uk-UA",
        "ro-RO", "el-GR", "cs-CZ", "hu-HU", "he-IL", "ta-IN", "te-IN", "ml-IN", "kn-IN",
        "gu-IN", "pa-IN", "sr-RS", "sk-SK", "sl-SI", "bg-BG", "hr-HR", "lt-LT", "lv-LV",
        "et-EE", "am-ET", "sw-KE", "zu-ZA", "xh-ZA", "so-SO", "yo-NG", "ig-NG", "af-ZA",
        "az-AZ", "kk-KZ", "uz-UZ", "mn-MN", "my-MM", "km-KH", "lo-LA", "si-LK", "ne-NP",
        "ps-AF", "dv-MV", "ha-NE", "ti-ET", "hy-AM", "ka-GE", "be-BY", "bs-BA", "mk-MK",
        "ga-IE", "cy-GB", "sq-AL", "is-IS", "mt-MT", "lb-LU", "eo-EO", "la-LA", "gl-ES",
        "eu-ES", "ca-ES", "sa-IN", "bo-CN", "mi-NZ", "qu-PE", "ay-BO", "gn-PY", "ug-CN",
        "ug-UZ", "ku-TR", "ckb-IQ", "nah-MX", "sm-WS", "fj-FJ", "haw-US", "lus-IN", "mni-IN",
        "sat-IN", "br-FR", "oc-FR", "rm-CH", "jv-ID", "su-ID", "ceb-PH", "ilo-PH", "hil-PH",
        "war-PH", "pam-PH", "bcl-PH", "tgl-PH", "mr-IN", "as-IN"
    ]
    print("\n🌍 Select a language:")
    for idx, lang in enumerate(languages):
        print(f"{idx + 1}. {lang}")
    while True:
        try:
            choice = int(input("Enter language number: "))
            if 1 <= choice <= len(languages):
                return languages[choice - 1]
            else:
                print("❌ Invalid number. Try again.")
        except ValueError:
            print("⚠ Please enter a valid number.")