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
from langchain_openai import OpenAIEmbeddings

import dotenv

def rag_with_log(question):

    # Define the metadata extraction function.
    def metadata_func(record: dict, metadata: dict) -> dict:

        metadata["timestamp"] = record.get("timestamp")
        metadata["source"] = record.get("source")
        metadata["movieDetails"] = record.get("movieDetails")
        metadata["searchTerm"] = record.get("searchTerm")
        metadata["error"] = record.get("error")
        metadata["level"] = record.get("level")


        return metadata


    loader = JSONLoader(
        file_path='../graylog_rest_api/log.json',
        jq_schema='.data[]',
        content_key="message",
        metadata_func=metadata_func
    )

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain =  (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain)

    response = rag_chain_with_source.invoke(question)

    vectorstore.delete_collection()

    return response

def rag_with_code(question):
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
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)
    len(texts)

    vectorstore = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
    retriever = vectorstore.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8},
    )

    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain =  (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain)

    response = rag_chain_with_source.invoke(question)

    vectorstore.delete_collection()
    return response


if __name__=='__main__':
    dotenv.load_dotenv()


    resp1 = rag_with_log("When I try to fetch movie details it does not show me the movie detail, instead I get something like undefined. This is the log. help me to find the possible causes and show me the log")

    # print(resp1)

    resp2 = rag_with_code("show me which part of the code that gives me error, and show me how to fix this. this is the previous context " + str(resp1))
    print(resp2)

