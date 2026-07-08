import chromadb

COLLECTION_NAME = "Tutorial-Agentic-AI"

client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection(COLLECTION_NAME)

collection.add(
    documents=[
        "This is the first document.",
        "This is the second document.",
        "This is the third document.",
    ],
    metadatas=[
        {"source": "my_source_1"},
        {"source": "my_source_2"},
        {"source": "my_source_3"},
    ],
    ids=["doc1", "doc2", "doc3"],
)

results = collection.query(
    query_texts=["This is a document."],
    n_results=2,
)

print(f"Connected to remote Chroma at localhost:8000")
print(f"Collection: {COLLECTION_NAME}")
print(results)
print("-----\n")

for document in results["documents"]:
    for doc in document:
        print(doc)
        print("-----\n")
