"""
social_agent.py
===============

`generate_social_calendar()`:
1.  Scrapes a URL
2.  Summarises the company in <150 words
3.  Generates N platform-specific posts based on a date/weekly schedule

Used by `src.cli` for a simple command-line interface.
"""
from __future__ import annotations

import json
import os
from typing import Dict

from dotenv import load_dotenv
load_dotenv()  # Loads OPENAI_API_KEY and USER_AGENT from .env
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader

from .schedule_builder import build_schedule


# --------------------------------------------------------------------------- #
# 1.  Shared LLM instance
# --------------------------------------------------------------------------- #
llm = ChatOpenAI(model_name="gpt-4o-mini")  # swap to gpt-4o (no "-mini") in prod

# --------------------------------------------------------------------------- #
# 2.  Prompt templates
# --------------------------------------------------------------------------- #
SUMMARY_PROMPT = PromptTemplate.from_template(
    """
You are analysing a company website.

URL: {url}
Raw page text (may be truncated): {page_text}

Write a concise (<150 words) summary focusing on:
  • what the company does
  • flagship products / services
  • sustainability or innovation angles
"""
)

POST_PROMPT = PromptTemplate.from_template(
    """
You are an expert {platform} content strategist.
Create {n_posts} posts – one per entry in schedule_list – and return **valid JSON**
exactly in this shape:

{{
  "posts": [
    {{
      "label": "",      // Monday / Week 1 etc.
      "hook": "",       // Thumb-stopping opener
      "caption": "",    // Main copy
      "visual": "",     // Image / video idea
      "hashtags": []    // List of hashtags
    }}
  ]
}}

**Do NOT wrap the JSON in markdown backticks.**

Company summary:
{company_summary}

Extra info from user (optional):
{extra_info}

Schedule:
{schedule_list}
"""
)

# --------------------------------------------------------------------------- #
# 3.  Small helper
# --------------------------------------------------------------------------- #
def _to_str(msg) -> str:
    """Unwrap an AIMessage (or passthrough str)."""
    return msg.content if hasattr(msg, "content") else str(msg)


# --------------------------------------------------------------------------- #
# 4.  Public coroutine
# --------------------------------------------------------------------------- #
async def generate_social_calendar(
    *,
    n_posts: int,
    interval: str,
    url: str,
    platform: str = "instagram",
    extra_info: str = "",
) -> Dict:
    """
    Return a dict produced from LLM-generated JSON.

    Raises:
        • ValueError           – if schedule arguments are invalid
        • json.JSONDecodeError – if the LLM outputs invalid JSON
    """
    # 4-a. Build labels like ['Monday', …] or ['Week 1', …]
    schedule = build_schedule(n_posts, interval)

    # 4-b. Scrape the page
    loader = WebBaseLoader(url)  # picks up USER_AGENT from env vars internally
    page_text = loader.load()[0].page_content

    # Optional: keep prompt payload small
    page_text = page_text[:4000]  # chars

    # 4-c. Summarise
    summary_msg = (SUMMARY_PROMPT | llm).invoke(
        {"url": url, "page_text": page_text}
    )
    company_summary = _to_str(summary_msg)

    # 4-d. Generate posts
    posts_msg = (POST_PROMPT | llm).invoke(
        {
            "platform": platform,
            "n_posts": n_posts,
            "schedule_list": schedule,
            "company_summary": company_summary,
            "extra_info": extra_info,
        }
    )
    raw_json = _to_str(posts_msg)

    # 4-e. Parse and return
    return json.loads(raw_json)
