from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from chains import get_generate_tweet_chain, get_reflection_chain

load_dotenv()

REFLECT = "reflect"
GENERATE_TWEET = "generate_tweet"


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def generate_tweet_node(state: State):
    response = get_generate_tweet_chain().invoke({"messages": state["messages"]})
    return {"messages": [response]}


def reflect_node(state: State):
    result = get_reflection_chain().invoke({"messages": state["messages"]})
    return {"messages": [HumanMessage(content=result.content)]}


def should_continue(state: State) -> Literal["reflect", "__end__"]:
    if len(state["messages"]) > 6:
        return END
    return REFLECT


builder = StateGraph(State)
builder.add_node(GENERATE_TWEET, generate_tweet_node)
builder.add_node(REFLECT, reflect_node)
builder.add_edge(START, GENERATE_TWEET)
builder.add_conditional_edges(GENERATE_TWEET, should_continue, {END: END, REFLECT: REFLECT})
builder.add_edge(REFLECT, GENERATE_TWEET)

graph = builder.compile()

if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())
    graph.get_graph().print_ascii()

    inputs = {
        "messages": [
            HumanMessage(
                content="Write a tweet about how AI agents are changing software development."
            )
        ]
    }
    for event in graph.stream(inputs):
        print(event)
        print("----")
