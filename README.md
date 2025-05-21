# CSO Provision Classifier
This project extracts and classifies legal provisions from international nonprofit laws using a hybrid approach combining manual control, OpenAI's GPT models, and the CSO Regulatory Regime Matrix.

## Purpose
To automatically classify legal provisions from international nonprofit-related laws according to permissiveness vs. restrictiveness and their subgroup (formation, governance, operations, resources). The classification is grounded in the CSO Matrix typology, which is stored in data/cso-matrix.txt and used during inference via the OpenAI responses.create() API.

## Getting started
### Step 1: Install dependencies
pip install -r requirements.txt

### Step 2: Add your OpenAI API key
Create a .env file in the root directory with the following content:
api_key=your-openai-api-key
This is used in classifier.py via os.getenv("api_key") to keep your key secure.

### Step 3: Run the Example Classifier
python main.py
This will classify a sample provision hardcoded in main.py using the logic from classifier.py.

## Other Scripts (in pdf_scripts/)
These are in development and support additional workflows. (Extracting provisions from PDFs, detecting provision boundaries via layout spacing and preparing training data for ML-based filtering)

## Outputs
Outputs are printed to terminal by default. You can modify main.py to classify provisions from a list, file, or a full PDF pipeline (in progress)

## Contributing
Feel free to open issues or submit pull requests. You can add more country-specific extraction logic, improve classification output structure, or extend support for batch classification.