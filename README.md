# Travel Advisor Chatbot

A Streamlit-based travel chatbot that combines:

- Local travel knowledge files
- Wikipedia retrieval for selected destinations
- A local Ollama LLM via LangChain

## Tech Stack

- Python
- Streamlit
- LangChain (`langchain-core`, `langchain-community`, `langchain-ollama`)
- Ollama (`gemma2:2b`)
- ChromaDB

## Features

- Chat-style travel Q&A interface
- Hybrid retrieval:
  - Wikipedia context for known destination names
  - Local text knowledge base for general travel queries
- Prompt-based response generation with conversation history

## Project Structure

- `travelBot.py` - Main Streamlit app and routing logic
- `Asia Destinations.txt` - Asia destination knowledge
- `Europe Destinations.txt` - Europe destination knowledge
- `Travel Advice.txt` - General travel advice knowledge
- `requirements.txt` - Python dependencies

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd TravelBot
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Pull the Ollama model used by this app:

```bash
ollama pull gemma2:2b
```

5. Run the app:

```bash
streamlit run travelBot.py
```

## Notes

- The app now uses project-relative file paths, so it is portable after cloning.
- If Ollama is not running, LLM responses will fail. Start Ollama before launching the app.
