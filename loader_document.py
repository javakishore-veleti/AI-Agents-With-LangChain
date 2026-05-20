import tempfile

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader

def load_temp_text_file():
    """Creates a temporary text file for demonstration purposes"""
    sample_content = "This is a sample document loaded using TextLoader."
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
        temp_file.write(sample_content)
        temp_file_path = temp_file.name
    return temp_file_path

def demo_document_loader(file_path:str = "sample.txt"):
    print(f"Demonstrating document loading using TextLoader...{file_path}")
    """Demonstrates loading a document using a document loader"""
    loader = TextLoader(file_path)
    documents = loader.load()
    for doc in documents:
        print(f"Document metadata: {doc.metadata}")
        print(f"Document content: {doc.page_content}")
        print("---")
        print(f"Document content: {doc.page_content}")

if __name__ == "__main__":
    load_dotenv()
    temp_file_path = load_temp_text_file()
    demo_document_loader(temp_file_path)