import chromadb
import os
from dotenv import load_dotenv
from pdf_to_text import Pdf_to_text
from csv_functions import Csv_to_list
load_dotenv()
def context_provider(query:str,filename = None):
    if filename is None or filename == "":
        return "File not provided."
    if filename.split(".")[-1] == "csv":
        chunks=Csv_to_list(filename) 
        if chunks=="File not found":
            return chunks
        ids=[str(n+1)for n in range(len(chunks))]
        no_result=3
    elif filename.split(".")[-1] == "pdf":
        signal=Pdf_to_text(filename)
        if signal == "File not found":
            return signal
        if signal is True:
            with open(f"./text_of_pdf/{filename}_output.txt","r",encoding="utf-8") as file:
                contents=file.read()
            def split_text(contents, chunk_size=800, overlap=90):
                chunks = []
                start = 0
                while start < len(contents):
                    end = start + chunk_size
                    chunks.append(contents[start:end])
                    start += chunk_size - overlap
                return chunks
            chunks=split_text(contents)
            # print("len of chunks:",len(chunks))
            ids=[str(i+1) for i in range(len(chunks))]
            # print(len(ids))
        no_result=2
    else:
        return "not .pdf or .csv file"
    client = chromadb.PersistentClient(path="./chroma_db")
    collection_name=filename.replace(" ","_").replace("(","-").replace(")","-").replace("/","-").replace(":","-").replace("[","_").replace("]","_").replace("+","_")
    status=True
    if collection_name in [collection.name for collection in client.list_collections()]:
        status=False
        collection=client.get_collection(name=collection_name)
    if status:
        collection = client.create_collection(
        name=collection_name,
        # embedding_function=embedding_function
        )
        collection.add(ids=ids,documents=chunks)
    results=collection.query(query_texts=[query],n_results=no_result)
    threshold_distance=1.5
    if not results["distances"] or not results["distances"][0]:
        return ["No matching documents found."]
    print("Distance:",results["distances"][0][0])
    if results["distances"][0][0] < threshold_distance:
        return results["documents"]
    else:
        return ["not relevant context."]





