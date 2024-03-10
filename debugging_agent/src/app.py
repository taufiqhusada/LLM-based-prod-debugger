
from flask import Blueprint, request, jsonify
import os
from flask import Flask
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_core.messages import AIMessage, HumanMessage,  get_buffer_string

from get_vector_log import load_vectorstore_log
from get_vector_codebase import load_vectorstore_codebase

from defer import defer

from operator import itemgetter

from langchain.globals import set_verbose, set_debug
import json


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Backend is active'


@app.route('/ask', methods=['POST'])
def do_conversation():
    # set_verbose(True)
    # set_debug(True)
    data = request.json

    conversation = data['conversation']
    question = data['question']
    source = data['source']

    chat_history = []
    for item in conversation:
        if item["role"] == "user":
            chat_history.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            chat_history.append(AIMessage(content=item["content"]))
    
    retriever = None
    vectorstore = None

    if (source == 'code'):
        retriever, vectorstore = load_vectorstore_codebase()
    else :
        retriever, vectorstore = load_vectorstore_log()

    print(retriever, vectorstore)

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    qa_system_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

                            Question: {question} 

                            Context: {context} 

                            Answer:"""


    contextualize_q_system_prompt = """Given a chat history and the latest user question \
                                        which might reference context in the chat history, formulate a standalone question \
                                        which can be understood without the chat history. Do NOT answer the question, \
                                        just reformulate it if needed and otherwise return it as is.
                                        
                                        Chat History:
                                        {chat_history}
                                        Follow Up Input: {question}
                                        Standalone question:"""
    
    # Now we calculate the standalone question
    _inputs = RunnableParallel(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: get_buffer_string(x["chat_history"])
        ) | ChatPromptTemplate.from_template(contextualize_q_system_prompt) | llm | StrOutputParser(),)
    

    # Now we retrieve the documents
    retrieved_documents = {
        "docs": itemgetter("standalone_question") | retriever,
        "question": lambda x: x["standalone_question"],
    }

    
    # Now we construct the inputs for the final prompt
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    final_inputs = {
        "context": lambda x: format_docs(x["docs"]),
        "question": itemgetter("question"),
    }

    # And finally, we do the part that returns the answers
    answer = {
        "answer": final_inputs | ChatPromptTemplate.from_template(qa_system_prompt) | llm,
        "docs": itemgetter("docs"),
    }

    # And now we put it all together!
    final_chain = _inputs | retrieved_documents | answer

    
    response = final_chain.invoke({
        "question": question,
        "chat_history":chat_history,
    })

    vectorstore.delete_collection()

    print(response)

    return jsonify({
        "response": response["answer"].content,
        "docs": json.dumps([ob.__dict__ for ob in response["docs"]])
    })

if __name__ == '__main__':
    app.run(debug=True)