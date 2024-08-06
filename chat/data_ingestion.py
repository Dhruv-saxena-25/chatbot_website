from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chat.data_converter import dataconverter
import os

from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT=os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE=os.getenv("ASTRA_DB_KEYSPACE")

gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def data_ingestion(status):

    vstore = AstraDBVectorStore(
        embedding=gemini_embeddings,
        collection_name = "bot",
        api_endpoint = ASTRA_DB_API_ENDPOINT,
        token = ASTRA_DB_APPLICATION_TOKEN,
        namespace = ASTRA_DB_KEYSPACE 
    )

    storage = status

    if storage == None:
        docs = dataconverter() 
        insert_ids = vstore.add_documents(docs)
    
    else:
        return vstore
    return vstore, insert_ids

if __name__ == "__main__":

    vstore, insert_ids = data_ingestion(None)
    print(f"\n Inserted {len(insert_ids)} documents.")
    results = vstore.similarity_search("Who is cherry?")
    for res in results:
        print(f"\n {res.page_content} [{res.metadata}]")
