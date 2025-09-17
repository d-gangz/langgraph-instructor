"""
Builds upon 2-tools.py by adding memory.

Added memory to the chatbot. And ok I checked Langsmith and there is the proven caching that is happening. So everything seems to be working. I have a basic reAct agent with memory working.
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from tavily import TavilyClient
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


graph_builder = StateGraph(MessagesState)

tavily_client = TavilyClient()


@tool
def tavily_search(query: str, max_results: int | None = None) -> dict:
    """Search using Tavily API with specified query and max results.
    Args:
        query: The search query to find relevant information
        max_results: Maximum number of search results to return. Optional, defaults to 2 if not specified.
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

tools = [tavily_search]

llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are a helpful assistant that can use tools to get information.
Before you call a tool, explain why you are calling it
"""


def chatbot(state: MessagesState):
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


# running the chatbot
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [HumanMessage(content=user_input)]}, config):
        for value in event.values():
            # print("Assistant:", value["messages"][-1].content)
            # using this way, u can see the tool calls and results
            print("Assistant:", value["messages"][-1])


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
