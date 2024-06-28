from langchain.memory.buffer import ConversationBufferMemory
from langchain.memory.kg import ConversationKGMemory
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import (AIMessagePromptTemplate,
                               SystemMessagePromptTemplate,
                               HumanMessagePromptTemplate,PromptTemplate,ChatPromptTemplate,
                               MessagesPlaceholder)
from langchain_core.messages import (HumanMessage,AIMessage,SystemMessage)

import src.sourcefiles as sf
import src.llm_models as llmmodels
import os
import uuid
from dotenv import load_dotenv
load_dotenv()
role_message=''' you are an expert data analyst, proficient in various task such as
                           question-answering,text-generation, summarization, data extraction, name-entity-recognition,
                           document abstract writing, document introduction writing.
                           use the provided context to answer questions in a conversional and concise manner:
                           {context}

'''
contextualize_system_prompt =SystemMessage (content='''
    Given a chat history and the latest user question 
    which might reference context in the chat history,
    formulate a standalone question which can be understood
    without the chat history. Do NOT answer the question,
    just reformulate it if needed and otherwise return it as is.'''
)
def chat_chain(path:str, query:str,llm_provider:str='google',retriever_provider:str='chroma',
                model_id:str='gemini-pro',emb_id:str='models/embedding-001'):
    docs=sf.get_document(path)
    llmmodel,chatmodel,embeding=llmmodels.get_model(llm_provider,model_id,emb_id)
    retriever=sf.get_retriever(retriever_provider,docs,embeding)
    stuff_prompt=ChatPromptTemplate.from_messages([
        ('system',role_message),
        MessagesPlaceholder(variable_name='chat_history'),
        HumanMessage(content='''{input}''')
    ])
    contxt_propmt=ChatPromptTemplate.from_messages([
        contextualize_system_prompt,
        MessagesPlaceholder(variable_name='chat_history'),
        ("human",'{input}')
    ])
    history_awre_retriever=create_history_aware_retriever(chatmodel,retriever,contxt_propmt)
    stuff_chain=create_stuff_documents_chain(chatmodel,stuff_prompt)
    rag_chain=create_retrieval_chain(history_awre_retriever,stuff_chain)
    store = {}
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )
    sessionkey=uuid.uuid4()
    chain_result=conversational_rag_chain.invoke({'input':query},
                                                 config={'configurable':{'session_id':'ses123'}})
    return chain_result['answer'],docs
def ret_chain(path:str, query:str,llm_provider:str='google',retriever_provider:str='chroma',
                model_id:str='gemini-pro',emb_id:str='models/embedding-001'):
    docs=sf.get_document(path)
    llmmodel,chatmodel,embeding=llmmodels.get_model(llm_provider,model_id,emb_id)
    retriever=sf.get_retriever(retriever_provider,docs,embeding)
    stuff_prompt=PromptTemplate.from_template(template=role_message+'\n'+'{input}')
    stuff_chain=create_stuff_documents_chain(llmmodel,stuff_prompt)
    rag_chain=create_retrieval_chain(retriever,stuff_chain)
    
    chain_result=rag_chain.invoke({'input':query})
    return chain_result['answer'],docs
