"""
⏱ Duration Selection Module

Allows users to select the desired duration (in seconds) for their generated voice file.
"""

def select_duration(default=15):
    print("\n⏳ Enter the desired voice duration in seconds.")
    print(f"(Press Enter to use default duration: {default} seconds)")

    while True:
        user_input = input("Duration (in seconds): ").strip()
        if not user_input:
            return default
        try:
            duration = int(user_input)
            if duration > 0:
                return duration
            else:
                print("⚠ Please enter a positive integer.")
        except ValueError:
            print("⚠ Invalid input. Please enter a valid number.")