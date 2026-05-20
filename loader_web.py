from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader


def demo_web_loader(url: str = "https://www.example.com"):
    """Demonstrates loading a web page using WebBaseLoader"""
    print(f"Demonstrating web loading using WebBaseLoader...{url}")
    loader = WebBaseLoader(url, bs_kwargs={"parse_only": None})
    documents = loader.load()
    for doc in documents:
        print(f"Document metadata: {doc.metadata}")
        print(f"Document content: {doc.page_content}")
        print("---")
        print(f"Document content: {doc.page_content}")


if __name__ == "__main__":
    load_dotenv()
    demo_web_loader()
