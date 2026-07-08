import chromadb

collections = chromadb.Client().create_collection("Tutorial-Agentic-AI")

collections.add(
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

results = collections.query(
    query_texts=["This is a document."],
    n_results=2,
)

print(results)
print("-----\n")
documents = results['documents']
for document in documents:
    for doc in document:
        print(doc)
        print("-----\n")
