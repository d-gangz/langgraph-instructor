from typing import Annotated

from langgraph import graph
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Image, display
from langsmith.wrappers import wrap_openai

load_dotenv()


class State(
    TypedDict
):  # Messages have the type "list". The `add_messages` function # in the annotation defines how this state key should be updated # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

client = wrap_openai(OpenAI())


def chatbot(state: State) -> State:
    # Convert LangGraph messages to OpenAI responses API format
    # For multi-turn conversations, we need to format messages properly
    if len(state["messages"]) == 1:
        # Single message - use simple string input
        user_msg = state["messages"][0]
        if hasattr(user_msg, "content"):
            input_text = user_msg.content
        else:
            input_text = user_msg["content"]
    else:
        # Multi-turn conversation - format as messages array
        messages = []
        for msg in state["messages"]:
            if hasattr(msg, "type") and hasattr(msg, "content"):
                # LangGraph message object - convert to responses API format
                messages.append({"role": msg.type, "content": msg.content})
            elif isinstance(msg, dict) and "role" in msg and "content" in msg:
                # Already in correct format
                messages.append(msg)
        input_text = messages

    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        text={"verbosity": "low"},
        input=input_text,
    )

    # Return the response in LangGraph format
    # GPT-5 responses API returns output_text, not choices
    return {"messages": [{"role": "assistant", "content": response.output_text}]}


graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            # Handle both LangGraph message objects and dict responses
            last_msg = value["messages"][-1]
            if hasattr(last_msg, "content"):
                print("Assistant:", last_msg.content)
            else:
                print("Assistant:", last_msg["content"])


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
