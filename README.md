# CSO Provision Classifier
This project classifies legal provisions from international nonprofit laws using OpenAI's GPT models.

## Purpose
To automatically classify legal provisions from international nonprofit-related laws according to permissiveness vs. restrictiveness and their subgroup:
- Formation
- Governance 
- Operations
- Resources 

The classification is grounded in the CSO Matrix typology, which is stored in data/cso-matrix.txt and used via the OpenAI responses.create() API.

## Tools and project background
This project is built in Python due to its flexibility, strong ecosystem for text processing, and widespread adoption in machine learning. It uses the OpenAI Responses API to leverage the use of large language models (LLMs) for classifying legal provisions.

#### What is "cloning a repository"?
Cloning means making a full copy of this project from GitHub to your computer. We do this so you can run or edit the files locally. It’s like downloading a folder of tools that someone built and shared online. You can either:

- Use a program called Git to clone.
- Simply click “Download ZIP” on the GitHub page and extract the folder. (If you install VS Code like in the instructions below, it will open there!)

#### What Is the OpenAI API (and Why Do I Need It)?
This project uses OpenAI's API, which is a service that lets your computer ask a powerful language model (LLM) for answers.
- LLM (Large Language Model): A type of AI trained to understand and generate human language. In this case, it's trained to read legal provisions and classify them according to regulatory categories.
- API (Application Programming Interface): A way for your computer to communicate with OpenAI’s servers. When you run the tool, it sends the provision text to OpenAI’s model and gets a structured answer in return.
- You need an OpenAI account with an API key to use this service.
This key is like a personal password that allows your computer to use OpenAI's model securely.

## Getting started
### What you need
1. Python (programming language)
    - Needed to run the scripts.
    - Download from [python.org](https://www.python.org/).
    - On Windows, check the box "Add Python to PATH" during installation.
2. VS Code or another IDE (Integrated Development Environment)
    - To open, edit, and run the scripts easily.
    - Recommended: [VS Code](https://code.visualstudio.com/).
    - Install Python extension when prompted.
3. Git (optional but helpful)
    - To clone the GitHub project.
    - Download from [git-scm](https://git-scm.com/).
    - If for any reason you skip Git, you can just download your repo as a ZIP from GitHub. However, we recommed installing it as it makes cloning this repository easier.
4. OpenAI API Key
    - Needed to call the classification model.
    - Get it from [OpenAI platform](https://platform.openai.com/api-keys).
    - You will need a personal API key.

And you're all set up!

### Step 1: Cloning the GitHub Repository
To get started, you need a copy of this project on your computer.

- Option A: If you have Git installed

    Open a terminal and run:

    ```
    git clone https://github.com/raulpzs/cso-classifier.git
    cd cso-classifier 
    ```

- Option B: If you don't have Git installed

    - Go to https://github.com/raulpzs/cso-classifier
    - Click the green "Code" button  and select "Download ZIP"
    - Unzip the folder
    - Open it in VS Code or another IDE.

### Step 2: Install dependencies
This project uses the openai library and other packages listed in requirements.txt.
To install them, open a terminal inside the project folder and run:

    pip install -r requirements.txt

This will install the openai library and other requirements.

### Step 3: Add your OpenAI API key

The `.env` file is a safe way to store sensitive information (like your OpenAI key) without putting it directly in the code. It lets the script use your key without exposing it publicly.

To do this, create a `.env` file in the root directory (main folder) with just the following content inside:
`api_key=your-openai-api-key` and you're done.

This is used in classifier.py via `os.getenv("api_key")` to keep your key secure.

### Step 4: Run the Example Classifier
You can now classify your own provision directly from the terminal by running:

    python main.py "Any provision you want"

for example,

    python main.py "A nonprofit may receive donations without prior approval."

This will use the classifier and print a structured classification result.

## Other Scripts (in pdf_scripts/)

This folder contains in-development tools for more advanced tasks:
- Extracting provisions from PDFs
- Detecting provision boundaries based on layout and visual spacing
- Preparing training data for machine learning-based filtering

These are optional and not required to use the core classifier.

## Outputs
Outputs are printed to terminal by default. You can modify main.py to classify provisions from a list, file, or a full PDF pipeline (in progress). These are not required to use the core classifier.

## Contributing
Feel free to open issues or submit pull requests. You can add more country-specific extraction logic, improve classification output structure, or extend support for batch classification from PDFs.