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
```
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
├── .env.example              # Example environment variables
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sultan9723/Vocalforge_Agent.git
cd Vocalforge_Agent
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
```

5. Verify setup:
```bash
python scripts/generate_voices.py 001
```

## API Keys Setup

- **OpenAI**: Get your API key from https://platform.openai.com/api-keys
- **Gemini**: Get your API key from https://makersuite.google.com/app/apikey  
- **Azure Speech**: Create a resource at https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices

For multiple API keys (for rate limit rotation), separate them with commas in your .env file:
```
AZURE_API_KEY=key1,key2,key3
GEMINI_API_KEY=key1,key2
```

## Usage

1. Prepare input
   - Add text files or prompts into input/ (or configure paths in the script).

2. Run voice generation
   ```bash
   python scripts/generate_voices.py
   ```

3. Expanded workflows
   - **Gemini expansion**: expand_inputs_gemini.py expands topics into longer text.
   - **Duration control**: expand_inputs_to_target_duration.py ensures outputs match desired length.
   - **Input fixing**: fill_input_files.py auto-corrects or populates missing inputs.

## Security
- Secrets and keys are never committed to git.
- .gitignore ensures sensitive and large folders (.env, voices/, output/, temp/) are excluded.
- GitHub push protection prevents accidental secret leaks.

## Contribution
Pull requests are welcome. Please follow code formatting and ensure no secrets are pushed.
