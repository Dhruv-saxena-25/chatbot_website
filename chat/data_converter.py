from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def dataconverter():
    data_file = "./data\\Dhruv Saxena.docx"
    loader = Docx2txtLoader(data_file)
    data = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=200)
    chunks = splitter.split_documents(data)
    return chunks

   

