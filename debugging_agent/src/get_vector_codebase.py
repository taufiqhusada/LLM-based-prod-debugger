import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_core.runnables import RunnableParallel

from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings




def load_vectorstore_codebase():
    repo_path = "/Users/taufiq/Documents/Research/prod debugger/sample_buggy_app"
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".js"],
        exclude=["node_modules/*/*", "node_modules/*/*/*", "node_modules/*/*/*/*", "node_modules/*/*/*/*/*"],
        parser=LanguageParser(language=Language.JS, parser_threshold=500),
    )
    documents = loader.load()
    

    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JS, chunk_size=1000, chunk_overlap=200,  add_start_index = True
    )
    texts = python_splitter.split_documents(documents)

    identifier = 0
    for t in texts:
        t.metadata.update({"source": t.metadata.get("source") + "_chunk_" + str(identifier)})
        identifier+=1
   

    # vectorstore = Chroma.from_documents(texts, embedding_fuction=HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2"), persist_directory="./chroma_db/codebase/sentence-transformer")
    vectorstore = Chroma.from_documents(texts, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db/codebase/openai")
    retriever = vectorstore.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8},
    )
    return retriever, vectorstore