"""
Code guide for the recipe retrieval file:
- Imports the embedding model, vector database, document wrapper, os, and pandas.
- Loads the CSV recipe dataset.
- Creates embeddings for each recipe.
- Uses a local Chroma folder for persistence.
- Builds documents and IDs from the CSV rows.
- Adds recipe documents to Chroma and exposes a retriever for top matches.
"""

from langcahin_ollama import OllamaEmbeddings
from langcahin_chroma import CHroma
from langchain_core.documents import Document
import os
import pandas as pd 



df = pd.read_csv("korean_food_recipes.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for index, row in df.iterrows():
        document = Document(
            page_content=row["title"] + "\n" + row["ingredients"] + "\n" + row["instructions"],
            id = str(index)
        )
        ids.append(str(i))
        documents.append(document)

    
    vector_store = Chroma(
        collection_name="Korean food recipes",
        persist_directory=db_location,
        embedding_function=embeddings   

    )

    if add_documents:
        vectore_store.add_documents(documents, ids=ids)
    
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
        
    )
