from dotenv import load_dotenv
from importlib.metadata import version
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def demo_stream_execution():
    """Demonstrates streaming execution of a chain using LCEL and Runnable"""

    # Component 1: Define the prompt template
    prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Answer in one sentence {question}")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    parser = StrOutputParser()
    chain = prompt | model | parser

    # Stream execution with a question
    question = {"question": "What is the capital of France?"}
    for result in chain.stream(question):
        print(result, end="", flush=True)


if __name__ == "__main__":
    load_dotenv()
    demo_stream_execution()
