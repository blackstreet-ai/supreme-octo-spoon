# Case in Point Script Generator

This project is an AI-powered workflow for transforming news articles into polished YouTube narration scripts, styled for the "Case in Point" channel. It is built with the OpenAI Agents SDK and demonstrates modular, agentic orchestration with tool use, fact-checking, and brand voice adaptation.

## Features

- **Interactive CLI**: Prompts the user for a news article URL to process.
- **Multi-Agent Pipeline**: Orchestrates a sequence of agents for:
  - Article ingestion and cleaning
  - Research and fact gathering
  - Outline and script drafting
  - Brand voice/style polishing
  - Fact-checking and citation
- **OpenAI + Tools**: Integrates OpenAI models (e.g., GPT-4.1) and custom tools for web search, HTML fetching, and style retrieval.
- **Markdown Output**: Outputs the final narration script as markdown (`script.md`), ready for editing or direct use.
- **Traceable Runs**: Each workflow run is traced and viewable in the OpenAI dashboard for debugging and review.

## Usage

1. **Install dependencies** (see requirements.txt)
2. **Set your OpenAI API key** in a `.env` file:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. **Run the workflow:**
   ```sh
   python main.py
   ```
4. **Paste a news article URL** when prompted.
5. **View the generated script** in `script.md`.

## Project Structure
- `main.py` — Entry point, agent orchestration, and CLI
- `tools.py` — Custom tools (web search, fetch_url, style retriever)
- `assets/` — Style guide markdown
- `docs/` — Extended documentation and SDK references

## Extending
- Add new tools or agents in `tools.py` and `main.py`
- Customize agent instructions for different styles or workflows
- See `docs/` for more on the OpenAI Agents SDK

---

**Created with OpenAI Agents SDK.**
