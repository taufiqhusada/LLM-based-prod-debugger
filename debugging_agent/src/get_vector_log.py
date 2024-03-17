import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings



def load_vectorstore_log():
     # Define the metadata extraction function.
    def metadata_func(record: dict, metadata: dict) -> dict:

        metadata["timestamp"] = record.get("timestamp")
        metadata["source"] = record.get("source")
        metadata["movieDetails"] = record.get("movieDetails")
        metadata["searchTerm"] = record.get("searchTerm")
        metadata["error"] = record.get("error")
        metadata["level"] = record.get("level")
        metadata["gl2_message_id"] = record.get("gl2_message_id")


        return metadata


    loader = JSONLoader(
        file_path='../temp/log.json',
        jq_schema='.data[]',
        content_key="message",
        metadata_func=metadata_func
    )

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    # vectorstore = Chroma.from_documents(splits, embedding_function=HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2"), persist_directory="./chroma_db/logs/sentence-transformer")

    vectorstore = Chroma.from_documents(splits, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db/logs/openai")

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()

    return retriever, vectorstore