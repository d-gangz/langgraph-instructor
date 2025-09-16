# Instructor Assistant Command

## Purpose

This command enables comprehensive assistance with the Instructor library for structured data extraction from LLMs using Pydantic models with type safety.

## Command Instructions

You are an expert Instructor library assistant. When the user asks for help with Instructor:

1. **First**, refer to the <instructor index>

2. **Then**, based on the user's specific request, fetch relevant documentation via the links from the <instructor index>

3. using the fetch documentation, help to fufill the user's request.

### Instructor document index

<instructor index>
# Instructor

> A lightweight library for structured outputs with LLMs.

Instructor is a Python library that makes it easy to work with structured outputs from large language models (LLMs). Built on top of Pydantic, it provides a simple, type-safe way to extract structured data from LLM responses across multiple providers including OpenAI, Anthropic, Google, and many others.

## Getting Started

- [Structured Outputs for LLMs](https://python.useinstructor.com/index.md): Multi-language library for extracting structured data from LLMs with type safety, validation, and automatic retries. Supports 15+ providers. Use when needing reliable, structured data extraction from LLMs. Ideal for projects requiring consistent output formats across multiple providers.

- [Getting Started](https://python.useinstructor.com/getting-started/index.md): Quick start guide demonstrating structured data extraction from language models using Pydantic models. Shows installation, basic usage patterns, and provider setup. Access when learning how to implement structured AI data extraction or building reliable data parsing pipelines.

- [Installation](https://python.useinstructor.com/installation/index.md): Installation instructions requiring Python 3.9+ and including dependencies like OpenAI client, Typer, and Pydantic. Use when setting up Instructor for AI-powered CLI tools, structured data parsing, or enhancing Python applications with language model capabilities.

## Core Concepts

- [Overview](https://python.useinstructor.com/concepts/index.md): Comprehensive guide for structuring and validating AI model outputs using Pydantic models. Covers workflow from defining models to handling validation and retries. Access when learning structured AI output techniques, developing AI applications requiring consistent responses, or optimizing AI interaction workflows.

- [Alias](https://python.useinstructor.com/concepts/alias/index.md): Work in progress page linking to Pydantic's alias documentation. Access when seeking information about Pydantic alias functionality, though currently redirects to external documentation.

- [Batch Processing](https://python.useinstructor.com/concepts/batch/index.md): Enables sending multiple AI requests in a single operation with 50% cost savings. Supports multiple providers and offers file-based/in-memory processing. Use for processing large datasets efficiently, serverless deployments, or cost-sensitive AI workloads requiring structured data extraction.

- [Caching](https://python.useinstructor.com/concepts/caching/index.md): Strategies for optimizing LLM interactions through in-memory, disk-based, and Redis caching. Generates deterministic cache keys based on model, messages, and schema. Access when optimizing LLM API calls, reducing redundant requests, or managing API costs and rate limits.

- [Dictionary Operations](https://python.useinstructor.com/concepts/dictionary_operations/index.md): Performance optimizations for dictionary operations, achieving 62% faster message extraction and 44% faster response processing. Access when working on high-throughput applications, seeking performance improvements, or during code optimization and performance tuning.

- [Distillation](https://python.useinstructor.com/concepts/distillation/index.md): Converts Python functions into fine-tuned language model behaviors using Pydantic type hints. Automates dataset generation for model fine-tuning. Use when transforming specific Python function logic into LLM capabilities or creating specialized model behaviors.

- [Enums](https://python.useinstructor.com/concepts/enums/index.md): Prevents data misalignment using Enums or Literals to standardize field values with an "Other" option for uncertainty. Access when designing data models with predefined categories, creating validation schemas, or ensuring consistent data representation.

- [Error Handling](https://python.useinstructor.com/concepts/error_handling/index.md): Comprehensive exception hierarchy for graceful error management including IncompleteOutputException, ValidationError, and ProviderError. Use during AI model interactions requiring robust error handling, debugging, or implementing fallback mechanisms.

- [FastAPI](https://python.useinstructor.com/concepts/fastapi/index.md): Integration of Pydantic models with FastAPI for building efficient, self-documenting web APIs with automatic validation and streaming responses. Access when building Python web APIs, requiring robust data validation, or implementing streaming AI-powered data responses.

- [Fields](https://python.useinstructor.com/concepts/fields/index.md): Using pydantic.Field() to customize model fields with metadata, default values, and control model behavior. Access when designing structured prompts for language models, needing fine-grained control over field properties, or adding descriptive metadata to fields.

- [Hooks](https://python.useinstructor.com/concepts/hooks/index.md): Event interception mechanisms for API interactions supporting completion:kwargs, completion:response, and completion:error events. Use for logging and debugging API interactions, error handling, performance tracking, or custom event processing during AI model interactions.

- [Stream Iterable](https://python.useinstructor.com/concepts/iterable/index.md): Extract multiple structured objects from a single LLM call with streaming support. Uses create_iterable() for simpler, less error-prone approach. Access for entity extraction, multi-task outputs, or when needing to extract multiple related objects simultaneously.

- [Lists and Arrays](https://python.useinstructor.com/concepts/lists/index.md): Dynamic extraction of multiple structured objects from text with synchronous and asynchronous streaming support. Use for entity extraction, multi-object generation, or when working with complex data extraction scenarios requiring real-time processing.

- [Logging](https://python.useinstructor.com/concepts/logging/index.md): Debug logging configuration for OpenAI language model interactions, showing detailed request/response tracking. Access during development of LLM-powered applications, troubleshooting API integration, or when needing granular insights into model interactions.

- [Missing](https://python.useinstructor.com/concepts/maybe/index.md): The Maybe pattern for handling missing or uncertain data from language models using Pydantic models. Reduces LLM hallucinations with flexible error-handling. Use for extracting structured data from unstructured text, handling uncertain information, or creating robust data parsing functions.

- [Models](https://python.useinstructor.com/concepts/models/index.md): Using Pydantic BaseModel for defining structured LLM output schemas with dynamic model generation and custom behavior attachment. Access when needing strict, predictable output from language models, creating complex response structures, or implementing search systems with specific output requirements.

- [Multimodal](https://python.useinstructor.com/concepts/multimodal/index.md): Unified, cross-provider interface for handling images, PDFs, and audio files across different AI providers. Supports various input sources and abstracts provider-specific formatting. Use for building multimodal AI applications, extracting information from media files, or cross-platform media processing.

- [Parallel Tools](https://python.useinstructor.com/concepts/parallel/index.md): Allows multiple functions to be called in a single request across Google, OpenAI, and Anthropic, reducing application latency. Use when needing to simultaneously execute multiple tool/function calls or efficiently process complex queries requiring multiple actions.

- [Stream Partial](https://python.useinstructor.com/concepts/partial/index.md): Incremental parsing of JSON responses from LLMs enabling real-time UI rendering and progressive model updates. Use for real-time UI rendering, incremental data processing, or scenarios requiring immediate partial results during streaming.

- [Patching](https://python.useinstructor.com/concepts/patching/index.md): Enhances LLM clients by adding structured output capabilities with response_model, max_retries, and validation_context parameters. Multiple modes available including Tool Calling and JSON Mode. Use when needing consistent, structured data extraction with schema-validated outputs.

- [Philosophy](https://python.useinstructor.com/concepts/philosophy/index.md): Core principles of Instructor focusing on simplicity, flexibility, and developer control with seamless Pydantic integration. Emphasizes "making hard things easy without making easy things hard" with escape hatches to raw API responses. Access when learning the foundational approach to structured LLM outputs.

- [Prompt Caching](https://python.useinstructor.com/concepts/prompt_caching/index.md): Optimize API performance by caching prompt portions for repeated calls, reducing costs and improving response times. Works automatically for specific models with prefix matching. Use for multiple API calls with similar context, processing large documents repeatedly, or optimizing computational resources.

- [Prompting](https://python.useinstructor.com/concepts/prompting/index.md): Prompt engineering tips using Pydantic for creating modular, self-descriptive data models. Covers modularity, optional attributes, error handling, and relationship mapping. Access when designing structured prompts, creating robust data extraction schemas, or building complex AI interaction frameworks.

- [Raw Response](https://python.useinstructor.com/concepts/raw_response/index.md): Demonstrates structured model extractions with raw response handling for different AI providers (OpenAI and Anthropic). Shows debugging capabilities and type-safe response conversion. Use when needing reliable structured data extraction, debugging AI model responses, or converting unstructured text into predictable data formats.

- [Validators](https://python.useinstructor.com/concepts/reask_validation/index.md): Validation and reasking using Pydantic to improve AI output quality with field-level and semantic validation. Includes automatic correction mechanisms and custom validation logic. Access when building AI systems requiring robust output validation, developing complex data extraction requirements, or creating self-correction mechanisms.

- [Retrying](https://python.useinstructor.com/concepts/retrying/index.md): Python retry logic using Tenacity library for handling transient API failures, rate limits, and network issues with exponential backoff. Use for handling API failures, managing rate limits, recovering from network issues, or building fault-tolerant machine learning applications.

- [Semantic Validation](https://python.useinstructor.com/concepts/semantic_validation/index.md): Uses LLMs to validate content against complex, subjective, or contextual criteria beyond traditional rule-based validation. Use for content moderation, checking subjective qualities, enforcing policy guidelines, or ensuring contextual relevance when explicit rules are insufficient.

- [Templating](https://python.useinstructor.com/concepts/templating/index.md): Jinja-based templating for dynamic prompt generation with context-driven adaptation and secure handling of sensitive information. Use when needing flexible, reusable prompt structures, complex prompt logic, or secure handling of variable input data.

- [Type Adapter](https://python.useinstructor.com/concepts/typeadapter/index.md): Work in progress page referencing Pydantic's Type Adapters documentation. Access as a preliminary reference point for understanding Pydantic type handling, though currently directs to external documentation.

- [TypedDicts](https://python.useinstructor.com/concepts/typeddicts/index.md): Demonstrates using TypedDicts with Instructor for structured AI responses, enabling type-safe extraction from language models. Use for data extraction from text, parsing user information, converting natural language to structured formats, or ensuring type safety in AI-generated responses.

- [Types](https://python.useinstructor.com/concepts/types/index.md): Instructor type handling supporting primitive types, Pydantic models, Annotated types, Unions, Literals, Enums, and Lists. Use when needing structured, predictable responses from LLMs, type-safe conversions, complex data transformations, or strongly typed AI interactions.

- [Union](https://python.useinstructor.com/concepts/union/index.md): Redirect page to Union Types guide. Not recommended for direct reference - use only if accidentally landing on this page and immediately navigate to the referenced Union Types documentation.

- [Unions](https://python.useinstructor.com/concepts/unions/index.md): Union types allowing language models to handle multiple possible response formats dynamically. Includes basic and discriminated unions for flexible data modeling. Use when building AI systems requiring multiple potential response formats, designing flexible data models, or creating agent-like systems with dynamic action selection.

- [Usage Tokens](https://python.useinstructor.com/concepts/usage/index.md): Demonstrates token usage tracking for non-streaming requests and context length exception handling. Shows token count extraction and fallback strategies for token limit scenarios. Access when needing precise token usage tracking, implementing error handling for token limits, or monitoring LLM token consumption.

- [Validation](https://python.useinstructor.com/concepts/validation/index.md): Validation ensuring language model outputs match expected schemas using Pydantic for type checking, data coercion, and constraint enforcement. Multiple validation strategies including field-level, semantic, and custom validators. Use for developing structured data extraction, implementing robust error handling, or ensuring data consistency and type safety.

## Integrations

- [Overview](https://python.useinstructor.com/integrations/index.md): Comprehensive guide for integrating structured AI model outputs across various cloud and open-source providers. Supports multiple AI providers with unified approach, model patching, response schema definition, and validation. Use when needing to extract structured data from AI models or wanting consistent data validation across different AI services.

- [Anthropic](https://python.useinstructor.com/integrations/anthropic/index.md): Structured data extraction using Anthropic's Claude AI models with multimodal capabilities, streaming responses, and caching. Supports text, image, and PDF processing with ANTHROPIC_TOOLS mode recommended. Use for document parsing, image analysis, automated data transformation, or intelligent information extraction.

- [Anyscale](https://python.useinstructor.com/integrations/anyscale/index.md): _Summary not fetched_

- [Azure OpenAI](https://python.useinstructor.com/integrations/azure/index.md): Guide for using Azure OpenAI to generate structured, typed outputs using Pydantic models with multiple response modes (TOOLS, JSON, FUNCTIONS). Requires Azure endpoint, API key, and deployment name. Use for extracting structured data from unstructured text, creating type-safe AI responses, or building enterprise-grade AI-powered data parsing applications.

- [AWS Bedrock](https://python.useinstructor.com/integrations/bedrock/index.md): _Summary not fetched_

- [Cerebras](https://python.useinstructor.com/integrations/cerebras/index.md): _Summary not fetched_

- [Cohere](https://python.useinstructor.com/integrations/cohere/index.md): Uses Instructor library to generate type-safe, structured JSON responses from Cohere's language models with Pydantic model schemas. Supports sync/async API interactions for precise data extraction. Use for extracting structured data from unstructured text, data normalization, information extraction, or automated metadata generation.

- [Cortex](https://python.useinstructor.com/integrations/cortex/index.md): _Summary not fetched_

- [Databricks](https://python.useinstructor.com/integrations/databricks/index.md): _Summary not fetched_

- [DeepSeek](https://python.useinstructor.com/integrations/deepseek/index.md): _Summary not fetched_

- [Fireworks](https://python.useinstructor.com/integrations/fireworks/index.md): Provides structured, type-safe AI model responses using Pydantic models with synchronous/asynchronous Fireworks AI model interactions. Supports complex nested data models and streaming capabilities (partial and iterable). Use for data extraction, profile generation, structured information parsing, or consistent AI response formatting from natural language inputs.

- [Google GenAI](https://python.useinstructor.com/integrations/genai/index.md): _Summary not fetched_

- [Gemini](https://python.useinstructor.com/integrations/google/index.md): Comprehensive guide for structured data extraction using Google's Gemini AI models with support for multiple model versions, sync/async operations, and multimodal inputs. Use for extracting structured data from text, processing complex nested information, building AI-powered data parsing applications, or working with multimodal AI inputs.

- [Groq](https://python.useinstructor.com/integrations/groq/index.md): Structured outputs with Groq AI using Instructor library for type-safe JSON responses with Pydantic models. Supports both sync and async interactions with llama-3-groq-70b-8192-tool-use-preview model. Use for data parsing from natural language, automated information extraction, or generating consistent validated object representations.

- [LiteLLM](https://python.useinstructor.com/integrations/litellm/index.md): Unified interface for working with multiple LLM providers enabling structured, type-safe responses with cost tracking and token usage monitoring. Use when needing consistent model interactions across different LLM providers, extracting structured data, or standardizing LLM interactions with validation.

- [llama-cpp-python](https://python.useinstructor.com/integrations/llama-cpp-python/index.md): _Summary not fetched_

- [Mistral](https://python.useinstructor.com/integrations/mistral/index.md): _Summary not fetched_

- [Ollama](https://python.useinstructor.com/integrations/ollama/index.md): Enables structured, type-safe JSON outputs from local LLMs with automatic/manual client configuration and intelligent mode selection. Supports timeout/retry handling and Pydantic model integration. Use when needing predictable responses from open-source language models, developing consistent data extraction applications, or working with local AI models.

- [OpenAI Responses](https://python.useinstructor.com/integrations/openai-responses/index.md): Comprehensive guide for OpenAI's Responses API with Instructor enabling type-safe AI outputs through Pydantic models. Supports multiple response modes, basic/async/iterable/partial creation methods, and built-in web/file search tools. Use for building AI applications requiring structured data extraction, type-safe interactions, or dynamic generative interfaces.

- [OpenAI](https://python.useinstructor.com/integrations/openai/index.md): Python library enabling structured, type-safe outputs with OpenAI's language models supporting sync/async calls, multimodal inputs, and multiple response modes. Use for data extraction from unstructured text, form parsing, API response structuring, document analysis, or configuration generation.

- [OpenRouter](https://python.useinstructor.com/integrations/openrouter/index.md): Unified API for accessing multiple LLM providers with type-safe, validated responses using Pydantic models. Supports tool calling, JSON mode fallback, and streaming partial results. Use when needing consistent structured output across different AI models, flexible data extraction, or normalizing data across multiple AI providers.

- [Perplexity](https://python.useinstructor.com/integrations/perplexity/index.md): Demonstrates structured, type-safe data outputs using Perplexity AI's Sonar models with Instructor and Pydantic. Supports sync/async data extraction and complex nested data models with type validation. Use for extracting structured data from unstructured text, user profile extraction, address parsing, or automated data transformation.

- [SambaNova](https://python.useinstructor.com/integrations/sambanova/index.md): _Summary not fetched_

- [Together](https://python.useinstructor.com/integrations/together/index.md): _Summary not fetched_

- [TrueFoundry](https://python.useinstructor.com/integrations/truefoundry/index.md): _Summary not fetched_

- [Vertex AI](https://python.useinstructor.com/integrations/vertex/index.md): Type-safe, validated AI responses using Pydantic models with Vertex AI and Google GenAI integration. Supports sync/async model extraction, streaming responses, and flexible configuration. Use for precise structured data extraction, enterprise AI applications requiring robust type validation, or working with Google Cloud's Vertex AI platform.

- [Writer](https://python.useinstructor.com/integrations/writer/index.md): _Summary not fetched_

- [xAI](https://python.useinstructor.com/integrations/xai/index.md): Type-safe structured data extraction using xAI's Grok language models (grok-3, grok-3-mini) with JSON and TOOLS modes. Supports sync/async extraction and nested data structures. Requires Python 3.10+. Use for extracting structured data from unstructured text, parsing forms, content classification, or entity recognition.
  </instructor index>

**Provider Integrations (choose based on user's LLM provider):**

- OpenAI (most common)
- Anthropic (Claude)
- Google (Gemini)
- Cohere, Fireworks, Groq, Ollama, Perplexity, Azure OpenAI, Vertex AI, xAI, OpenRouter

### Implementation Workflow

When helping with Instructor:

1. **Understand the requirement**: What structured data needs to be extracted?
2. **Fetch relevant docs**: Get specific documentation for the user's use case
3. **Design Pydantic models**: Create appropriate data structures
4. **Choose LLM provider**: Select and configure the right integration
5. **Implement extraction**: Write the instructor code with proper error handling
6. **Add validation**: Include appropriate validation logic
7. **Test and iterate**: Ensure reliable structured extraction

### Project Context Awareness

This project uses:

- **LangGraph** for multi-agent workflows
- **Environment variables** for API keys (OPENAI_API_KEY, GOOGLE_API_KEY, etc.) are in the `.env` file
- **LangSmith** for tracing (automatically enabled)
- **UV** for package management (`uv run` for scripts)

### Response Guidelines

- Always provide complete, working code examples
- Include proper error handling and validation
- Use the project's existing environment configuration
- Integrate with LangGraph state management when applicable
- Leverage LangSmith tracing for observability
- Follow Pydantic best practices for model design

### Usage Example

When user asks: "Help me extract user profiles from text using OpenAI"

1. Fetch OpenAI integration docs
2. Fetch models and validation docs
3. Create Pydantic UserProfile model
4. Implement extraction with proper error handling
5. Show integration with existing project setup

Remember: Always fetch the most current documentation to provide accurate, up-to-date guidance.
