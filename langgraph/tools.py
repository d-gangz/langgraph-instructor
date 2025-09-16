"""
Builds upon basic-chatbot.py by adding tools.

Input data sources: User input from command line interface
Output destinations: Console output for chat responses
Dependencies: OpenAI API key, LangSmith API key for tracing
Key exports: chatbot(), stream_graph_updates()
Side effects: Makes OpenAI API calls, prints to console
"""

from typing import Annotated

from dotenv import load_dotenv
from IPython.display import Image, display
from langchain_core.messages.utils import convert_to_openai_messages
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from tavily import TavilyClient  # type: ignore
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


class State(TypedDict):
    """State for the chatbot with tool calling support.

    Messages have the type "list". The `add_messages` function in the
    annotation defines how this state key should be updated (in this case,
    it appends messages to the list, rather than overwriting them).
    """

    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

client = wrap_openai(OpenAI())
tavily_client = TavilyClient()


def tavily_search(query: str, max_results: int | None = None) -> dict:
    """Search using Tavily API with specified query and max results."""
    if max_results is None:
        max_results = 2
    return tavily_client.search(query=query, max_results=max_results)


# OpenAI tool definition for Tavily search
tavily_search_tool = {
    "type": "function",
    "name": "tavily_search",
    "description": (
        "Search the web using Tavily API to get current information "
        "and relevant results."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": ("The search query to find relevant information"),
            },
            "max_results": {
                "type": "integer",
                "description": (
                    "Maximum number of search results to return. "
                    "Optional, defaults to 2 if not specified."
                ),
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

# LangGraph tools are functions that can be called directly
langgraph_tools = [tavily_search]
# OpenAI tools are tool definitions that can be called using the OpenAI API
openai_tools = [tavily_search_tool]


def chatbot(state: State) -> State:
    """Process user messages and generate responses using GPT-5."""
    # Convert LangGraph messages to OpenAI format using the proper utility
    openai_messages = convert_to_openai_messages(state["messages"])
    # print("Original openai_messages:", openai_messages)

    # Filter messages for Responses API - remove tool_calls field
    filtered_messages = []
    for msg in openai_messages:
        if msg["role"] == "assistant" and "tool_calls" in msg:
            # Keep assistant message but remove tool_calls field
            filtered_msg = {"role": msg["role"], "content": msg["content"]}
            filtered_messages.append(filtered_msg)
        elif msg["role"] == "tool":
            # Combine tool result with the previous assistant message
            # Format it to show this is a tool result, not just random text
            tool_result_content = (
                f"[Tool Result from {msg.get('name', 'tool')}]: {msg['content']}"
            )
            filtered_msg = {"role": "assistant", "content": tool_result_content}
            filtered_messages.append(filtered_msg)
        else:
            # Keep other messages as-is
            filtered_messages.append(msg)

    # assistant_count = len([m for m in openai_messages if m["role"] == "assistant"])
    # print(f"\n=== Iteration #{assistant_count} ===")
    # print("Filtered messages for Responses API:", filtered_messages)

    # Handle single message case - extract just the content as string
    if len(filtered_messages) == 1:
        input_text = filtered_messages[0]["content"]
    else:
        # Multi-turn conversation - use the filtered messages array
        input_text = filtered_messages

    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        instructions=(
            "You are a helpful assistant that can use tools to get information. "
            "Before you call a tool, explain why you are calling it"
        ),
        text={"verbosity": "low"},
        input=input_text,
        tools=openai_tools,  # type: ignore
    )

    # Convert GPT-5 Response API output to LangGraph-compatible format
    # Collect all content and function calls to create a single coherent message
    text_content = ""
    tool_calls = []

    for item in response.output:
        if item.type == "message":
            # Extract text content from message items
            for content_item in item.content:
                if content_item.type == "output_text":
                    text_content += content_item.text

        elif item.type == "function_call":
            # Collect all function calls
            tool_calls.append(
                {
                    "id": item.call_id,
                    "type": "function",
                    "function": {"name": item.name, "arguments": item.arguments},
                }
            )

    # Create a single assistant message with both content and tool calls
    assistant_message = {
        "role": "assistant",
        "content": text_content,
    }

    # Add tool_calls if any were made
    if tool_calls:
        assistant_message["tool_calls"] = tool_calls  # type: ignore

    return {"messages": [assistant_message]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(langgraph_tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    # Using prebuilt tools_condition since we convert to standard format
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")

compiled_graph = graph_builder.compile()

try:
    display(Image(compiled_graph.get_graph().draw_mermaid_png()))
except ImportError:
    # This requires some extra dependencies and is optional
    pass


def stream_graph_updates(user_message: str) -> None:
    """Stream updates from the graph for the given user input."""
    initial_state = {"messages": [{"role": "user", "content": user_message}]}
    for event in compiled_graph.stream(initial_state):  # type: ignore
        for value in event.values():
            # Handle both LangGraph message objects and dict responses
            last_msg = value["messages"][-1]
            if hasattr(last_msg, "content"):
                print("Assistant:", last_msg.content)
            else:
                print("Assistant:", last_msg["content"])


if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
        except KeyboardInterrupt:
            # fallback if input() is not available
            FALLBACK_INPUT = "What do you know about LangGraph?"
            print("User: " + FALLBACK_INPUT)
            stream_graph_updates(FALLBACK_INPUT)
            break
