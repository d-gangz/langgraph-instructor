"""
Basic LangGraph chatbot that uses OpenAI's GPT-5 Responses API with proper message conversion utilities.

Input data sources: User input from command line interface
Output destinations: Console output for chat responses
Dependencies: OpenAI API key, LangSmith API key for tracing
Key exports: chatbot(), stream_graph_updates()
Side effects: Makes OpenAI API calls, prints to console
"""

from typing import Annotated

from langgraph import graph
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Image, display
from langsmith.wrappers import wrap_openai
from langchain_core.messages.utils import convert_to_openai_messages

load_dotenv()


class State(
    TypedDict
):  # Messages have the type "list". The `add_messages` function # in the annotation defines how this state key should be updated # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

client = wrap_openai(OpenAI())


def chatbot(state: State) -> State:
    # Convert LangGraph messages to OpenAI format using the proper utility
    openai_messages = convert_to_openai_messages(state["messages"])

    # Handle single message case - extract just the content as string
    if len(state["messages"]) == 1:
        input_text = openai_messages[0]["content"]
    else:
        # Multi-turn conversation - use the converted messages array
        input_text = openai_messages

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
