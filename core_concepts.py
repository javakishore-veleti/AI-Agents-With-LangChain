from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def demo_basic_chain(question:str = "Default question"):
    """Demonstrates a basic chain using LCEL and Runnable"""

    # Component 1: Define the prompt template
    prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Answer in one sentence {question}")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    parser = StrOutputParser()
    chain = prompt | model | parser

    input_schema = chain.input_schema.model_json_schema()
    output_schema = chain.output_schema.model_json_schema()
    print(f"Input schema: {input_schema}")
    print(f"Output schema: {output_schema}")

    return chain

def main():
    print("Hello from ai-agents-with-langchain!")
    chain = demo_basic_chain()
    # You can also invoke the chain with a different question
    result = chain.invoke({"question": "What is the capital of India?"})
    print(f"Result from basic chain with new question: {result}")

if __name__ == "__main__":
    main()