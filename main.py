from dotenv import load_dotenv
from importlib.metadata import version

load_dotenv()

from langchain_core import __version__ as core_versioin
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def main():
    print("Hello from ai-agents-with-langchain!")
    print(f"Langchain Core version: {core_versioin}")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke("Say setup complete! in one word")
    print(f"Response from OpenAI: {response}")

    llm_anthropic = ChatAnthropic(model="claude-sonnet-4-5-20250929", temperature=0)
    response_anthropic = llm_anthropic.invoke("Say setup complete! in one word")
    print(f"Response from Anthropic: {response_anthropic}")


if __name__ == "__main__":
    main()
