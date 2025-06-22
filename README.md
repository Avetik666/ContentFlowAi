# ContentFlow AI – Social-Media Content Generator 🚀

Generate full content calendars (hooks, captions, visuals, hashtags) for any website in **one API call**.  
Powered by OpenAI + LangChain + LangGraph.

| Feature | Status |
|---------|--------|
| 1-shot CLI (JSON out) | ✅ |
| Sync FastAPI endpoint | ✅ |
| Redis-backed queue + worker | ✅ |
| Docker Compose stack | ✅ |
| Streaming tokens (SSE / WS) | ⬜ – easy to add later |

---

## 1. Quick start (local dev)

```bash
# clone & enter
git clone https://github.com/your-org/contentflow-ai.git
cd contentflow-ai

# Python ≥ 3.11 required
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# ① Add your keys
cp .env.example .env      # then edit .env

# ② Run the CLI
python3 -m src.cli \
  --url https://www.rtx.com \
  --platform instagram \
  --posts 3 \
  --interval day \
  --extra "focus on sustainability & hiring"
# ➜  prints JSON + writes calendar.json
```

### Dev tooling

```bash
pip install -r requirements-dev.txt
pre-commit install
```
# format everything
```ruff check . --fix && black . && isort .```

# run type checks
```mypy src/```

