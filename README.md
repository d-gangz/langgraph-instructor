# LangGraph + Instructor Playground

A playground project for experimenting with [LangGraph](https://github.com/langchain-ai/langgraph) and [Instructor](https://github.com/jxnl/instructor).

## What's This About

- **LangGraph**: Building multi-agent workflows with state management
- **Instructor**: Structured data extraction from LLMs using Pydantic models
- **LangSmith**: Observability and tracing for LLM applications
- **Goal**: Learn how these libraries work together for building performance agents

## Setup

Uses [uv](https://github.com/astral-sh/uv) for package management.

```bash
# Install dependencies
uv sync

# Run Python scripts
uv run script.py
```

## Environment

Copy `.env` and add your API keys:
- `OPENAI_API_KEY`
- `LANGSMITH_API_KEY` (optional, for tracing)