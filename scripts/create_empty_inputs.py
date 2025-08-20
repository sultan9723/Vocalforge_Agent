# create_empty_inputs.py
import os

folder = "inputs"
os.makedirs(folder, exist_ok=True)

# Create files input_229.txt to input_500.txt if they don't exist
for i in range(229, 501):
    path = os.path.join(folder, f"input_{i:03}.txt")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")  # Leave empty for now
print("✅ Empty files created from input_229.txt to input_500.txt")