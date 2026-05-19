from dotenv import load_dotenv
from importlib.metadata import version
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def demo_batch_execution():
    """Demonstrates batch execution of a chain using LCEL and Runnable"""

    # Component 1: Define the prompt template
    prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Answer in one sentence {question}")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    parser = StrOutputParser()
    chain = prompt | model | parser

    # Batch of questions to process
    batch_inputs = [
        {"question": "What is the capital of France?"},
        {"question": "What is the largest mammal?"},
        {"question": "What is the Capital of India?"},
    ]

    # Execute the chain on the batch of inputs
    results = chain.batch(batch_inputs)
    for result in results:
        print(f"Results: {result}")


if __name__ == "__main__":
    load_dotenv()
    demo_batch_execution()
