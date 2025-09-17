"""
Builds upon 3-memory.py by adding human in the loop.

Added human in the loop to the chatbot. it works quite well now. I can see the human in the loop working.
"""

from dotenv import load_dotenv
from IPython.display import Image, display
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt

load_dotenv()


graph_builder = StateGraph(MessagesState)

tavily_client = TavilyClient()


@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]


@tool
def tavily_search(query: str, max_results: int | None = None) -> dict:
    """Search using Tavily API with specified query and max results.

    Args:
        query: The search query to find relevant information
        max_results: Maximum number of search results to return.
            Optional, defaults to 2 if not specified.

    Returns:
        A dictionary containing the search results
    """
    if max_results is None:
        max_results = 2
    return tavily_client.search(query=query, max_results=max_results)


# using the gpt-5-nano model with the responses api
llm = ChatOpenAI(
    model="gpt-5-nano",
    use_responses_api=True,
)

tools = [tavily_search, human_assistance]

llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are a helpful assistant that can use tools to get information.
Before you call a tool, explain why you are calling it. Keep your responses short and concise. Don't be too verbose.
"""


def chatbot(state: MessagesState) -> dict:
    """Process messages with LLM and tools."""
    messages = state["messages"]
    # add the system prompt if it's not there
    if not (messages and messages[0].type == "system"):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


memory = InMemorySaver()

config = {"configurable": {"thread_id": "1"}}

# Define nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

# Define edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile(checkpointer=memory)

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass


while True:
    try:
        # Check if there's a pending interrupt first
        state = graph.get_state(config)

        if state.next:
            # We have a pending interrupt - go directly to resume flow
            print("🔄 Resuming from pending interrupt...")
            print("🤔 Please provide your expert guidance:")
            expert_input = input("> ")

            # Resume with expert input
            events = graph.stream(Command(resume={"data": expert_input}), config)

            # Stream the resumed events
            for event in events:
                for value in event.values():
                    if isinstance(value, dict) and "messages" in value:
                        print("Assistant:", value["messages"][-1])
        else:
            # Normal user input flow
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            # Start new conversation
            events = graph.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            )

            # Stream events
            for event in events:
                for value in event.values():
                    if isinstance(value, dict) and "messages" in value:
                        print("Assistant:", value["messages"][-1])

            # Check if execution was interrupted
            final_state = graph.get_state(config)
            if final_state.next:
                print("⏸️  Human assistance requested!")
                print("💡 Expert input needed - continuing to next prompt...")

    except KeyboardInterrupt:
        # fallback if input() is not available
        FALLBACK_INPUT = "What do you know about LangGraph?"
        print("User: " + FALLBACK_INPUT)
        events = graph.stream(
            {"messages": [HumanMessage(content=FALLBACK_INPUT)]}, config
        )
        for event in events:
            for value in event.values():
                if isinstance(value, dict) and "messages" in value:
                    print("Assistant:", value["messages"][-1])
        break
