# 🧠 Build an AI Agent in Python

This project is based on the **[Boot.dev](https://www.boot.dev)** course: [Build an AI Agent in Python](https://www.boot.dev/courses/build-ai-agent-python). 
It walks through building a simple AI agent from scratch using Python, with an emphasis on modular, testable code.

# IMPORTANT NOTICE

This project does NOT have all the security and safety features that a production AI agent would have. It is for learning purposes only. **Use at your own risk.**

## 🚀 What It Does

The AI agent is designed to perform tasks like:

- Parsing natural language input
- Executing tasks based on interpreted commands
- Storing and retrieving information from a memory-like structure
- Using basic reasoning to complete objectives

This project is educational and showcases how AI agents work at a conceptual level.

## Usage

1. **Install dependencies**  
   ```sh
   uv pip install -r requirements.txt
   ```

2. **Set up your `.env` file**  
   Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY="your-key-here"
   ```

3. **Run the AI bot with a your prompt**  
   ```sh
   uv run main.py "run calculator/tests.py"
   ```

   Or, to fix a bug in your code:
   ```sh
   uv run main.py "Fix the bug in calculator/pkg/calculator: 3 + 7 * 2 shouldn't be 20"
   ```

   To see verbose output:
   ```sh
   uv run main.py "run calculator/tests.py" --verbose
   ```

## 🛠️ Technologies Used

- Python 3.10+
- Command-line interface (CLI) tools (bash, git)
- Built-in Python libraries + Google's Gemini API

## 📁 Project Structure
```
bootdev-ai-bot/
├── call_function.py
├── config.py
├── functions/
│   ├── get_files_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
├── main.py
├── prompts.py
├── calculator/
│   ├── main.py
│   ├── tests.py
│   ├── lorem.txt
│   └── pkg/
│       ├── calculator.py
│       ├── render.py
│       └── morelorem.txt
├── .env
├── README.md
└── requirements.txt
```

- `main.py` — Entry point for the AI bot CLI
- `call_function.py` — Handles function calls and tool integration
- `config.py` — Configuration settings (e.g., set working directory)
- `functions/` — Modular function implementations for agent actions
- `prompts.py` — System prompt 
- `tests.py` — Unit and integration tests
- `.env` — Environment variables (API key)

## Planned Improvements
- [ ] Test the development environment setup to ensure it works seamlessly.
- [ ] Add a GIF demonstrating the usage of the application to `README.md`.
- [X] Include warnings or disclaimers in `README.md` (e.g., potential issues, limitations, or usage notes).
- [ ] Refactor the codebase to adhere to PEP8 standards.
- [ ] Write additional unit tests for critical components of the application.
- [ ] Improve security
