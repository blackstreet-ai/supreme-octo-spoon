from dotenv import load_dotenv
import os
from agents import Agent, Runner, trace
from tools import tavily_search, fetch_url, brand_style_retriever
import asyncio
# import logging
# logging.basicConfig(level=logging.DEBUG)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# --- Article‑Ingest ----------------------------------------------------------
article_ingest = Agent(
    name="article_ingest",
    instructions="""
    You are a news‑article ingestion bot.
    1. Receive {url}
    2. Download html, remove nav/ads, return clean markdown.
    Output JSON: {"article_md": "...", "title": "..."}
    """,
    model="gpt-4.1",
    tools=[fetch_url]
)

# --- Research ---------------------------------------------------------------
research = Agent(
    name="research",
    instructions="""
    Given {article_md} produce up to 5 bullet facts or contrasting viewpoints
    using the web‑search tool. Output JSON {"bullets":[...]}.
    """,
    model="gpt-4.1",
    tools=[tavily_search]
)

# --- Outline ---------------------------------------------------------------
draft_outline = Agent(
    name="draft_outline",
    instructions="""
    Turn {article_md} and {bullets} into a concise outline with:
      intro, 3‑5 section heads, outro CTA.
    Output {"outline":[...]}.
    """
)

# --- Script Writer ----------------------------------------------------------
script_writer = Agent(
    name="script_writer",
    instructions="""
    Expand {outline} into a 800‑1000‑word YouTube narration,
    2nd‑person POV, conversational, smart yet friendly.
    Return {"script": "..."}.
    """
)

# --- Style Polish -----------------------------------------------------------
style_polish = Agent(
    name="style_polish",
    instructions="""
    Adjust {script} to match the 'Case in Point' voice in the retrieved style doc.
    Keep timestamps for B‑roll notes in [BROLL: ] blocks.
    Return {"script_polished": "..."}.
    """,
    model="gpt-4.1",
    tools=[brand_style_retriever]
)

# --- Fact Check -------------------------------------------------------------
fact_check = Agent(
    name="fact_check",
    instructions="""
    For every statistic/quote in {script_polished} verify via web_search.
    Replace any unsupported claim with '[[needs verification]]'.
    Output {"script_checked": "...", "refs":[...]}.
    """,
    tools=[tavily_search]
)

# --- Citation ---------------------------------------------------------------
citation = Agent(
    name="citation",
    instructions="""
    Append numeric in‑line citations using {refs}. Output final script.
    """
)

# --- Orchestrator -----------------------------------------------------------
orchestrator = Agent(
    name="orchestrator",
    instructions="""
    Coordinate the tools to transform a URL into a finished narration script.
    """,
    model="o4-mini",
    tools=[
        article_ingest.as_tool("ingest", "Ingests an article from a URL and returns clean markdown and title."),
        research.as_tool("research", "Extracts up to 5 bullet facts or contrasting viewpoints from an article using web search."),
        draft_outline.as_tool("outline", "Creates a concise outline from article markdown and research bullets."),
        script_writer.as_tool("draft_script", "Expands an outline into a opinionated YouTube narration script."),
        style_polish.as_tool("polish", "Polishes the script to match the 'Case in Point' brand style, keeping B-roll notes."),
        fact_check.as_tool("fact_check", "Fact-checks statistics/quotes in the script using web search, marking unsupported claims."),
        citation.as_tool("cite", "Appends numeric in-line citations to the script using provided references.")
    ],
)

# --- Runner -----------------------------------------------------------------


async def main():
    USER_URL = input("Enter the article URL to process: ").strip()
    with trace("google_faces_off_flow"):
        result = await Runner.run(orchestrator, USER_URL)
    print(result.final_output)
    # Write the script output to script.md in markdown format (no code fences)
    with open("script.md", "w", encoding="utf-8") as f:
        f.write(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
