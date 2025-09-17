<!--
Document Type: Learning Notes
Purpose: Comprehensive guide for integrating OpenAI GPT-5 Responses API with LangGraph
Context: Created during implementation of tool-calling chatbot with GPT-5 and LangGraph
Key Topics: API integration, response format conversion, tool calling, error handling, best practices
Target Use: Reference guide for future development and troubleshooting
-->

# LangGraph + OpenAI GPT-5 Responses API Integration Guide

## Important Learnings

The key difficulty when using **LangGraph** with **OpenAI** is the message shape transformation. LangGraph uses LangChain's message format under the hood, which differs significantly from OpenAI's message format, especially with the Responses API.

This transformation is particularly challenging because when using the LangChain helpers, they don't transform properly for the Responses API. The conclusion is to use **LangGraph** with only a very primitive layer of **LangChain**. The issue with LangChain being overly abstracted becomes apparent when doing things that go beyond the primitive level.

**Key insight:** For advanced use cases like the GPT-5 Responses API, stick to LangGraph's core orchestration capabilities and implement the responses API using primitive Langchain.

## Overview

This document captures key learnings, patterns, and solutions discovered while integrating OpenAI's new GPT-5 Responses API with LangGraph for tool-calling applications.

## Table of Contents

1. [API Architecture Differences](#api-architecture-differences)
2. [Response Format Conversion](#response-format-conversion)
3. [Tool Calling Integration](#tool-calling-integration)
4. [Complex Scenarios Handling](#complex-scenarios-handling)
5. [Error Patterns and Solutions](#error-patterns-and-solutions)
6. [Best Practices](#best-practices)
7. [Performance Considerations](#performance-considerations)
8. [Code Examples](#code-examples)
9. [Troubleshooting Guide](#troubleshooting-guide)

## API Architecture Differences

### GPT-5 Responses API vs Chat Completions API

The GPT-5 Responses API introduces a fundamentally different response structure:

**Chat Completions API:**

```python
response = client.chat.completions.create(...)
message = response.choices[0].message
content = message.content
tool_calls = message.tool_calls  # Standard format
```

**GPT-5 Responses API:**

```python
response = client.responses.create(...)
# response.output is an array of Item objects
for item in response.output:
    if item.type == "message":
        # Extract text from content items
    elif item.type == "function_call":
        # Handle tool calls differently
```

### Key Structural Differences

| Aspect             | Chat Completions        | GPT-5 Responses         |
| ------------------ | ----------------------- | ----------------------- |
| Response Structure | `choices` array         | `output` array          |
| Message Format     | Single `message` object | Multiple `Item` objects |
| Content Access     | `message.content`       | `item.content[].text`   |
| Tool Calls         | `message.tool_calls`    | `function_call` items   |
| Reasoning          | Not available           | `reasoning` items       |

## Response Format Conversion

### The Core Challenge

LangGraph expects standard message formats with `tool_calls` attributes, but GPT-5 returns a different structure. The key insight is that **conversion is necessary** - you cannot use raw GPT-5 Response objects directly.

### Critical Error Without Conversion

```python
# L This FAILS - LangGraph can't handle raw Response objects
return {"messages": [response]}  # NotImplementedError: Unsupported message type
```

### Proper Conversion Pattern

```python
#  This WORKS - Convert to LangGraph format
def convert_gpt5_response(response):
    text_content = ""
    tool_calls = []

    for item in response.output:
        if item.type == "message":
            for content_item in item.content:
                if content_item.type == "output_text":
                    text_content += content_item.text

        elif item.type == "function_call":
            tool_calls.append({
                "id": item.call_id,
                "type": "function",
                "function": {
                    "name": item.name,
                    "arguments": item.arguments
                }
            })

    assistant_message = {
        "role": "assistant",
        "content": text_content,
    }

    if tool_calls:
        assistant_message["tool_calls"] = tool_calls

    return {"messages": [assistant_message]}
```

## Tool Calling Integration

### Tool Definition Differences

**GPT-5 Responses API (Internally Tagged):**

```python
{
    "type": "function",
    "name": "search_web",
    "description": "Search the web",
    "parameters": {...}
}
```

**Chat Completions API (Externally Tagged):**

```python
{
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the web",
        "parameters": {...}
    }
}
```

### LangGraph Tools Condition Integration

Once you convert GPT-5 responses to standard format, you can use LangGraph's prebuilt `tools_condition`:

```python
from langgraph.prebuilt import tools_condition

#  Works after proper conversion
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,  # Uses standard tool_calls detection
)
```

### Custom vs Prebuilt Conditions

**Initially considered:** Custom condition for GPT-5 format

```python
def custom_tools_condition(state):
    # Check for GPT-5 specific response format
    if hasattr(last_message, 'output'):
        for item in last_message.output:
            if item.type == "function_call":
                return "tools"
```

**Better approach:** Convert format + use prebuilt condition

- More maintainable
- Leverages LangGraph's battle-tested logic
- Works with ecosystem tools

## Complex Scenarios Handling

### Conversation History with Tool Results

**Critical Discovery:** The GPT-5 Responses API does NOT accept `tool_calls` fields or `tool` role messages in the input array. This causes errors:

```python
# ✗ This FAILS with "Unknown parameter: 'input[1].tool_calls'"
input_messages = [
    {"role": "user", "content": "What's the weather?"},
    {"role": "assistant", "tool_calls": [...], "content": "..."},  # ERROR
    {"role": "tool", "content": "..."}  # Also not recognized
]
```

**Solution:** Filter and transform messages before sending to Responses API:

```python
# ✓ This WORKS - Filter out tool_calls and convert tool messages
filtered_messages = []
for msg in openai_messages:
    if msg["role"] == "assistant" and "tool_calls" in msg:
        # Remove tool_calls field, keep only role and content
        filtered_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    elif msg["role"] == "tool":
        # Convert tool message to assistant message with labeled content
        tool_result_content = f"[Tool Result from {msg.get('name')}]: {msg['content']}"
        filtered_messages.append({
            "role": "assistant",
            "content": tool_result_content
        })
    else:
        # Keep other messages as-is
        filtered_messages.append(msg)
```

**Important Insights:**

1. **Label tool results clearly** (e.g., `[Tool Result from...]`) to prevent the model from making duplicate tool calls
2. **Tool role not supported** - Convert `tool` role messages to `assistant` role
3. **No tool_calls in input** - The Responses API generates tool calls but doesn't accept them in conversation history
4. **Prevents infinite loops** - Without proper labeling, the model may repeatedly call the same tool

### Multiple Tool Calls in Single Response

GPT-5 can return multiple `function_call` items in one response:

```python
# GPT-5 Response with multiple tools
response.output = [
    FunctionCall(name="search_web", arguments="..."),
    FunctionCall(name="get_weather", arguments="..."),
    Message(content="Let me search and check weather...")
]
```

**Key insight:** Collect ALL tool calls into single message:

```python
#  Correct: Single message with multiple tool_calls
assistant_message = {
    "role": "assistant",
    "content": text_content,
    "tool_calls": [tool_call_1, tool_call_2, ...]  # All in one message
}

# L Wrong: Separate messages for each tool call
messages = [
    {"role": "assistant", "tool_calls": [tool_call_1]},
    {"role": "assistant", "tool_calls": [tool_call_2]}
]
```

### Mixed Content Scenarios

GPT-5 can return both text explanation AND tool calls:

```python
response.output = [
    Message(content="I'll search for that information."),
    FunctionCall(name="search_web", arguments="...")
]
```

**Solution:** Aggregate all content into coherent message:

```python
# Combine text from all message items
text_content = ""
for item in response.output:
    if item.type == "message":
        for content_item in item.content:
            if content_item.type == "output_text":
                text_content += content_item.text

# Single coherent message with both text and tools
{
    "role": "assistant",
    "content": "I'll search for that information.",
    "tool_calls": [...]
}
```

## Error Patterns and Solutions

### Common Errors and Fixes

1. **Unsupported message type error**

   ```
   NotImplementedError: Unsupported message type: <class 'openai.types.responses.response.Response'>
   ```

   **Solution:** Convert GPT-5 Response to standard message format

2. **Type errors with tool_calls**

   ```
   error: Argument has incompatible type "dict[str, Sequence[Collection[str]]]"
   ```

   **Solution:** Add `# type: ignore` for complex tool call structures

3. **tools_condition not routing to tools**

   ```
   # GPT-5 made function call but routed to END instead of tools
   ```

   **Solution:** Ensure proper conversion creates `tool_calls` attribute

4. **Import errors with unused conditions**

   ```
   W0611: Unused tools_condition imported from langgraph.prebuilt
   ```

   **Solution:** Clean up imports when switching between custom/prebuilt

5. **Unknown parameter error with tool_calls**

   ```
   Error code: 400 - {'error': {'message': "Unknown parameter: 'input[1].tool_calls'."}}
   ```

   **Solution:** Filter out `tool_calls` from assistant messages before sending to Responses API

6. **Duplicate tool calls in conversation loop**
   ```
   # Model keeps calling the same tool repeatedly
   ```
   **Solution:** Label tool results clearly (e.g., `[Tool Result from...]`) when converting to assistant messages

### Debugging Techniques

1. **Log response structure**

   ```python
   for item in response.output:
       print(f"Item type: {item.type}")
       if hasattr(item, 'content'):
           print(f"Content: {item.content}")
   ```

2. **Verify message format**

   ```python
   print(f"Message has tool_calls: {'tool_calls' in assistant_message}")
   print(f"Tool calls count: {len(assistant_message.get('tool_calls', []))}")
   ```

3. **Test routing logic**
   ```python
   # Test what tools_condition returns
   result = tools_condition(state)
   print(f"Routing to: {result}")
   ```

## Best Practices

### API Configuration

1. **Use appropriate reasoning effort**

   ```python
   reasoning={"effort": "low"}  # For faster responses
   reasoning={"effort": "high"} # For complex tasks
   ```

2. **Add helpful instructions**

   ```python
   instructions="You are a helpful assistant that can use tools. Before calling a tool, explain why."
   ```

3. **Control verbosity**
   ```python
   text={"verbosity": "low"}   # Concise responses
   text={"verbosity": "high"}  # Detailed explanations
   ```

### Code Organization

1. **Separate conversion logic**

   ```python
   def convert_gpt5_response(response):
       # Dedicated conversion function
       pass

   def chatbot(state):
       response = client.responses.create(...)
       return convert_gpt5_response(response)
   ```

2. **Use type hints strategically**

   ```python
   def chatbot(state: State) -> State:
       # Clear function signatures
       pass
   ```

3. **Handle edge cases**
   ```python
   # Empty responses, missing content, etc.
   if not response.output:
       return {"messages": [{"role": "assistant", "content": ""}]}
   ```

### Development Workflow

1. **Test with direct execution**

   ```bash
   echo "test question" | uv run python langgraph/tools.py
   ```

2. **Use conventional commits**

   ```
   feat(tools): add GPT-5 integration
   fix(tools): handle multiple tool calls
   ```

3. **Wrap main execution**
   ```python
   if __name__ == "__main__":
       # Prevents execution during imports
   ```

## Performance Considerations

### GPT-5 Responses API Benefits

1. **Better caching:** 40-80% improvement over Chat Completions
2. **Chain of thought preservation:** Pass `previous_response_id` for continuity
3. **Lower latency:** Especially with `reasoning: {effort: "low"}`
4. **Cost efficiency:** Due to improved cache utilization

### Optimization Strategies

1. **Use appropriate model variants**

   ```python
   model="gpt-5"      # Complex reasoning tasks
   model="gpt-5-mini" # Balanced performance
   model="gpt-5-nano" # High-throughput tasks
   ```

2. **Configure for use case**

   ```python
   # Fast responses
   reasoning={"effort": "minimal"}
   text={"verbosity": "low"}

   # Thorough analysis
   reasoning={"effort": "high"}
   text={"verbosity": "high"}
   ```

3. **Leverage response chaining**
   ```python
   response2 = client.responses.create(
       previous_response_id=response1.id,  # Maintains context
       input="Follow up question"
   )
   ```

## Code Examples

### Complete Working Implementation

```python
from typing import Annotated
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from openai import OpenAI

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State) -> State:
    openai_messages = convert_to_openai_messages(state["messages"])

    # Filter messages for Responses API (remove tool_calls, convert tool messages)
    filtered_messages = []
    for msg in openai_messages:
        if msg["role"] == "assistant" and "tool_calls" in msg:
            filtered_messages.append({"role": msg["role"], "content": msg["content"]})
        elif msg["role"] == "tool":
            tool_result = f"[Tool Result from {msg.get('name')}]: {msg['content']}"
            filtered_messages.append({"role": "assistant", "content": tool_result})
        else:
            filtered_messages.append(msg)

    # Handle single vs multi-turn
    if len(filtered_messages) == 1:
        input_text = filtered_messages[0]["content"]
    else:
        input_text = filtered_messages

    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        instructions="You are a helpful assistant that can use tools.",
        text={"verbosity": "low"},
        input=input_text,
        tools=openai_tools,
    )

    # Convert GPT-5 format to LangGraph format
    text_content = ""
    tool_calls = []

    for item in response.output:
        if item.type == "message":
            for content_item in item.content:
                if content_item.type == "output_text":
                    text_content += content_item.text

        elif item.type == "function_call":
            tool_calls.append({
                "id": item.call_id,
                "type": "function",
                "function": {"name": item.name, "arguments": item.arguments},
            })

    assistant_message = {
        "role": "assistant",
        "content": text_content,
    }

    if tool_calls:
        assistant_message["tool_calls"] = tool_calls

    return {"messages": [assistant_message]}

# Build graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)

graph = graph_builder.compile()
```

### Tool Definition Template

```python
# OpenAI tool for GPT-5 Responses API
openai_tool = {
    "type": "function",
    "name": "function_name",
    "description": "Clear description of what the function does",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"],
        "additionalProperties": False,
    },
}

# LangGraph tool (actual function)
def function_name(param1: str) -> dict:
    """Function implementation."""
    return {"result": "data"}
```

## Troubleshooting Guide

### Quick Diagnostic Checklist

1. **Response format issues**

   - [ ] Are you converting GPT-5 Response to standard message format?
   - [ ] Are you handling both `message` and `function_call` items?
   - [ ] Are you aggregating content properly?

2. **Tool calling problems**

   - [ ] Are tool definitions in correct format (internally tagged)?
   - [ ] Are you collecting all tool calls into single message?
   - [ ] Is `tools_condition` detecting the `tool_calls` attribute?

3. **Import and type errors**
   - [ ] Are you importing `tools_condition` if using prebuilt?
   - [ ] Are you using `# type: ignore` for complex structures?
   - [ ] Are you cleaning up unused imports?

### Common Fixes

| Problem                       | Solution                                  |
| ----------------------------- | ----------------------------------------- |
| "Unsupported message type"    | Convert GPT-5 Response to standard format |
| Tools not being called        | Check tool_calls attribute in message     |
| Multiple tool calls splitting | Aggregate all calls into single message   |
| Type errors                   | Add strategic type ignores                |
| Import warnings               | Clean up unused imports                   |

### Testing Strategies

1. **Unit test conversion**

   ```python
   def test_response_conversion():
       mock_response = create_mock_gpt5_response()
       result = convert_gpt5_response(mock_response)
       assert "tool_calls" in result["messages"][0]
   ```

2. **Integration test**

   ```python
   def test_full_flow():
       result = graph.invoke({"messages": [{"role": "user", "content": "test"}]})
       assert result["messages"][-1]["role"] == "assistant"
   ```

3. **Manual testing**
   ```bash
   echo "Who won the NBA championship?" | uv run python app.py
   ```

## Migration Path

### From Chat Completions to GPT-5 Responses

1. **Update API calls**

   ```python
   # Before
   response = client.chat.completions.create(...)

   # After
   response = client.responses.create(...)
   ```

2. **Add conversion layer**

   ```python
   # Add response format conversion
   return convert_gpt5_response(response)
   ```

3. **Update tool definitions**

   ```python
   # Remove external function wrapper
   # Add proper parameter structures
   ```

4. **Test thoroughly**
   - Single tool calls
   - Multiple tool calls
   - Mixed content scenarios
   - Multi-turn conversations

## Future Considerations

### API Evolution

- Monitor OpenAI's Responses API updates
- New item types in `response.output`
- Additional reasoning capabilities
- Performance improvements

### LangGraph Integration

- Potential native GPT-5 support
- Enhanced tool calling features
- Better type safety

### Best Practices Evolution

- Response format standardization
- Error handling improvements
- Performance optimization patterns

---

## Conclusion

Integrating GPT-5 Responses API with LangGraph requires careful attention to response format conversion. The key insights:

1. **Conversion is mandatory** - raw GPT-5 responses don't work with LangGraph
2. **Aggregate content properly** - handle multiple items and tool calls correctly
3. **Use prebuilt components** - leverage `tools_condition` after proper conversion
4. **Test complex scenarios** - multiple tools, mixed content, error cases

This integration unlocks the performance benefits of GPT-5 Responses API while maintaining compatibility with LangGraph's powerful orchestration capabilities.

---

_Document created: 2025-01-16_
_Last updated: 2025-09-16_
_Version: 1.1_
