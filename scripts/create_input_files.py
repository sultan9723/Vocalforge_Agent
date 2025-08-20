import os

# Create "inputs" folder if it doesn't exist
os.makedirs("inputs", exist_ok=True)

# Generate 500 empty files: input_001.txt to input_500.txt
for i in range(1, 501):
    filename = f"inputs/input_{i:03}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")  # Leave it empty for now
print("✅ All 500 input files created in 'inputs/' folder.")