# VocalForge Agent
VocalForge Agent is a professional AI-powered voice generation pipeline designed for scalability and flexibility. It enables the creation of high-quality voice outputs with multiple providers, customizable voice parameters, and automated workflows for handling text and audio data efficiently.
## Features
- *Multi-provider support*: OpenAI, Azure, Gemini  
- *Voice customization*: Gender, accent, age, duration  
- *Config-driven*: Environment variable (.env) support for API keys and settings  
- *Automated workflows*:
- Input file formatting correction  
- Text expansion to meet target word/character count  
 - Empty file detection and fixing  
- Professional logging with colored terminal output  
- Extensible design: Easily add new voices or providers  
## Repository Structure
Vocalforge_Agent/
│
├── scripts/                 
│   ├── select_gender.py
│   ├── select_language.py
│   ├── select_duration.py
│   ├── select_accent.py
│   ├── select_age.py
│   ├── generate_voices.py
│   ├── expand_inputs_gemini.py
│   ├── expand_inputs_to_target_duration.py
│   └── fill_input_files.py
│
├── voices/                  # Generated voices (ignored in .gitignore)
├── output/                  # Final outputs (ignored in .gitignore)
├── temp/                    # Temporary files (ignored in .gitignore)
├── requirements.txt          # Python dependencies
## Installation
bash
# Clone repository
git clone https://github.com/sultan9723/Vocalforge_Agent.git
cd Vocalforge_Agent
# Set up virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
# Install dependencies
pip install -r requirements.txt
Environment Variables
Create a .env file in the project root. Use .env.example as a template:
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here
# Gemini
GEMINI_API_KEY=your_gemini_api_key_here
# Azure
AZURE_API_KEY=your_azure_api_key_here
AZURE_REGION=your_azure_region_here
AZURE_ENDPOINT=your_azure_endpoint_here
⚠ Do not commit your .env file — it’s ignored by .gitignore.
⸻
Usage
1. Prepare input
Add text files or prompts into input/ (or configure paths in the script).
2. Run voice generation
python scripts/generate_voices.py
3. Expanded workflows
	•	Gemini expansion: expand_inputs_gemini.py expands topics into longer text.
	•	Duration control: expand_inputs_to_target_duration.py ensures outputs match desired length.
	•	Input fixing: fill_input_files.py auto-corrects or populates missing inputs.
Security
	•	Secrets and keys are never committed to git.
	•	.gitignore ensures sensitive and large folders (.env, voices/, output/, temp/) are excluded.
	•	GitHub push protection prevents accidental secret leaks.
Contribution
Pull requests are welcome. Please follow code formatting and ensure no secrets are pushed.
├── .env.example              # Example environment variables
├── .gitignore
└── README.md
