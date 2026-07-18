from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()

assert os.getenv("GROQ_API_KEY") is not None, "GROQ_API_KEY environment variable is not set. Please set it in your .env file."

PDF_PATH = os.path.join(os.path.dirname(__file__), "data", "agentic-ai.pdf")
loader = PyPDFLoader(PDF_PATH)

pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,    # overlap keeps context at boundaries
    separators=["\n\n", "\n", ".", " "],  # tries paragraph → line → sentence → word
)

splits = text_splitter.split_documents(pages)

print(f"Total chunks: {len(splits)}  (from {len(pages)} pages)")
print(f"Avg chunk length: {sum(len(c.page_content) for c in splits) // len(splits)} chars")
print("\n--- Example chunk ---")
print(splits[5].page_content)