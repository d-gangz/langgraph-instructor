# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph + Instructor integration project for building structured LLM applications. The project is configured to use LangSmith for tracing and supports multiple LLM providers including OpenAI and Google AI.

## Development Environment

### Python Environment
- Use `uv` for package management and script execution
- Virtual environment is located in `.venv/`
- Run Python scripts with: `uv run <script_name>.py`
- Install dependencies with: `uv add <package_name>`

### Environment Configuration
- Copy `.env` file and configure API keys:
  - `OPENAI_API_KEY` - For OpenAI models
  - `GOOGLE_API_KEY` - For Google AI models
  - `LANGSMITH_API_KEY` - For LangSmith tracing
  - `LANGSMITH_PROJECT` - Set to "langgraph-instructor"
- LangSmith tracing is enabled by default (`LANGSMITH_TRACING=true`)

## Project Architecture

This project combines:
- **LangGraph**: For building multi-agent workflows and state management
- **Instructor**: For structured data extraction with Pydantic models
- **LangSmith**: For observability and tracing of LLM applications

## Key Dependencies

Based on the project focus, expect to work with:
- `langgraph` - Multi-agent workflow framework
- `instructor` - Structured LLM outputs with Pydantic
- `langchain` - LLM framework integration
- `pydantic` - Data validation and settings management
- `openai` - OpenAI API client
- `google-generativeai` - Google AI client

## Development Guidelines

### Code Organization
- Follow the Instructor pattern for structured data extraction
- Use LangGraph's StateGraph for multi-step workflows
- Implement proper error handling for LLM API calls
- Leverage Pydantic models for type safety and validation

### Testing
- Test LLM interactions with mock responses when possible
- Verify Pydantic model validation works correctly
- Test LangGraph state transitions and edge cases

### LangSmith Integration
- All LLM calls are automatically traced when `LANGSMITH_TRACING=true`
- Use descriptive run names for better observability
- Monitor token usage and latency through LangSmith dashboard