# tools.py
import os, json, httpx
from pathlib import Path
from typing import List, Dict

from agents import function_tool, WebSearchTool  # WebSearchTool is the hosted search tool

###############################################################################
# 1) Web search via OpenAI‑hosted tool (simplest)                              #
###############################################################################
# If you *don’t* want to pay for a Tavily key right now, just export the
# built‑in Hosted WebSearch tool so it can be used like a function tool.

tavily_search = WebSearchTool()  # ready‑made, no extra code needed


###############################################################################
# 2) Manual URL fetcher (scrapes raw HTML)                                    #
###############################################################################
@function_tool
async def fetch_url(url: str) -> str:
    """Download `url` and return the raw HTML as a string."""
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()
        return resp.text


###############################################################################
# 3) Brand‑style retriever (reads a local markdown guide)                     #
###############################################################################
STYLE_DOC_PATH = Path(__file__).parent / "assets" / "case_in_point_style.md"
STYLE_DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
STYLE_DOC_PATH.touch(exist_ok=True)  # creates an empty file the first time


@function_tool
def brand_style_retriever() -> str:
    """Return the channel’s style‑guide markdown."""
    return STYLE_DOC_PATH.read_text(encoding="utf‑8") or (
        "## Style guide\n\n(Add content to assets/case_in_point_style.md)"
    )
