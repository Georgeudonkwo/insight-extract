from types import NoneType
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.documents.base import Document
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.chroma import Chroma
from langchain_community.document_loaders.pdf import (PyPDFDirectoryLoader,
                                                      PyPDFLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.llm_models import google_embedding,google_models,GoogleVectorStore
from langchain_community.retrievers.google_vertex_ai_search import GoogleVertexAISearchRetriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_community.document_loaders.word_document import (UnstructuredWordDocumentLoader,
                                                                Docx2txtLoader)
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders.epub import UnstructuredEPubLoader
from langchain_community.document_loaders.email import UnstructuredEmailLoader
from langchain_community.document_loaders.csv_loader import CSVLoader,UnstructuredCSVLoader
from langchain_community.document_loaders.powerpoint import UnstructuredPowerPointLoader
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.wikipedia import WikipediaLoader
from langchain_community.retrievers.wikipedia import WikipediaRetriever
import os
from  typing import (List,Optional)
from dotenv import load_dotenv

_retriever_providers=['chroma','meta']
load_dotenv()
def chroma_retriever(docs,embeddings):
    retriever=Chroma.from_documents(documents=docs,embedding=embeddings).as_retriever()
    return retriever
def faiss_retriever(docs,embeddings):
    retriever=FAISS.from_documents(documents=docs,embedding=embeddings).as_retriever()
    return retriever
def get_retriever(provider:str,docs,embeddings):
    retriever=None
    if provider ==_retriever_providers[0]:
        retriever=chroma_retriever(docs,embeddings)
    elif provider ==_retriever_providers[1]:
        retriever=faiss_retriever(docs,embeddings)
    else:
        pass
    return retriever

def document_analyser_chain(llm,retriever,prompt):
    chain=({'context':retriever,'question':RunnablePassthrough()}
        |prompt|llm|StrOutputParser())
    return chain
def load_pdf(path:str):
    docs=PyPDFLoader(path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_txt(path:str):
    docs=TextLoader(path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_csv(path:str):
    docs=CSVLoader(path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_email(path:str):
    docs=UnstructuredEmailLoader(path,process_attachment=True).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_epud(path:str):
    docs=UnstructuredEPubLoader(path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_msword(path):
    docs=Docx2txtLoader(path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_excel(path):
    docs=UnstructuredExcelLoader(path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_webpages(url):
    docs=WebBaseLoader(url).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    return docs,splitdoc
def load_wiki(query:str):
    docs=WikipediaLoader(query).load()
    docs=[d for d in docs if not isinstance(d,NoneType)]
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    #res=[d for d in splitdoc if d is not None]
    return docs,splitdoc

def Load_PowerPoint(path):
    docs=UnstructuredPowerPointLoader(path).load()
    
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitdoc=splitter.split_documents(docs)
    print(splitdoc)
    print(len(splitdoc))
    return docs,splitdoc

wikiretriver=WikipediaRetriever()
wikiretriver
def get_document(path:str)->List[Document]:
    splitdoc_processed=None
    path=path.strip('"')
    if not os.path.isfile(path) and not path.startswith(('http','https')):
       try:
           try:
                _,splitdoc=load_wiki(path)
                splitdoc_processed='document is processed'
           except:
              raise Exception("wikipedia search engine failure")
               
       except:
            raise FileExistsError(f"file: {path} does not exist")
    _,ext=os.path.splitext(path)
    splitdoc=None
    if not splitdoc_processed:
        if ext.strip('.')=='pdf':
            _,splitdoc=load_pdf(path=path)
        elif ext.strip('.')=='txt':
            _,splitdoc=load_txt(path=path)
        elif ext.strip('.')=='csv':
            _,splitdoc=load_csv(path=path)
        elif ext.strip('.')=='docx':
            _,splitdoc=load_msword(path=path)
        elif ext.strip('.')=='xlsx':
            _,splitdoc=load_excel(path=path)
        elif ext.strip('.')=='epud':
            _,splitdoc=load_epud(path=path)
        elif ext.strip('.')=='pptx':
            _,splitdoc=Load_PowerPoint(path)
        elif path.startswith(('http','https')):
            _,splitdoc=load_webpages(path)
        else:
            raise AttributeError(f"file type {ext.strip('.')} is not supported")
    return splitdoc

prompt1=PromptTemplate(input_variables=['context','input','unknown'],
                          template=
                          ''' you are an expert analyst; you are good at varoius task such as:
                          summarization, text generation, feature extraction,name entity identification,
                          fact extraction and so on.
                          Use the provided datasource: {context}.
                          As your only source of truth to answer the 
                          question: {question}?.
                          if you do not know the answer, don't improvise, 
                          return:{unknown}
                          ''')
prompt=PromptTemplate(input_variables=['context','input'],
                          template=
                          ''' you are an expert analyst; you are good at various task such as:
                          summarization, text generation, feature extraction,name entity identification,
                          fact extraction,important points identification, important facts,discussions
                           of document abstract,discussion of document conclusion,discussing introduction,
                            mathematical analysis,identifying equations,analysing document introduction,
                            acronym recognition,
                             mathematical modelling, keypoint identification,
                             idea expansion, idea generation,hint generation,insight extraction,
                              careful reviewer, and general document analysis.
                              note: the following, criticalpressure is the same as pc
                          Use the provided datasource: [{context}],
                          as your only source of truth to answer the 
                          question: {question}?.
                          ''')


def analyse_documents(path:str,llm=None,embeddings=None,
                      llm_model_id="gemini-pro",
                      embedding_model_id='models/embedding-001',
                          retriever=None,prompt=prompt):
    splitdoc=get_document(path=path)
    llm=llm if llm else google_models(model_id=llm_model_id)
    embeddings=embeddings if embeddings else google_embedding(model_id=embedding_model_id)
    retriever=retriever if retriever else chroma_retriever(splitdoc,embeddings)
    chain=document_analyser_chain(llm=llm,retriever=retriever,prompt=prompt)
    return chain,splitdoc


if __name__=="__main__":
    #path=r"C:\Users\eno.udonkwo\Desktop\2023 Works\machine learning materials\1704.08863.pdf"
    #path=R"C:\Users\eno.udonkwo\Desktop\2024 works\(Studies in Computational Intelligence 385) Alex Graves (auth.) - Supervised Sequence Labelling with Recurrent Neural Networks-Springer-Verlag Berlin Heidelberg (2012).pdf"
    path=R"C:\Users\eno.udonkwo\Desktop\Employee Partnership Charter.docx"
    #path=R"C:\Users\eno.udonkwo\Downloads\CypherCrescent Strategic Employee Partnership Bonus.xlsxee"
    path=R"C:\Users\eno.udonkwo\Desktop\CypherCrescent Limited HSE Annual Report 2021-2022 .docx"
    path=r"https://www.fao.org/nigeria/fao-in-nigeria/nigeria-at-a-glance/en/"
    path=r"C:\Users\eno.udonkwo\Desktop\2023 Works\misc\Flare emission reduction utilizing solid oxide fuel cells at a natural gas.pdf"
    path='what is decarbonization'
    response=analyse_documents(path=path)
    query="mention atleast five important facts in the document"

   # print(response.invoke(query))
    #www=load_wiki('what is decarbonization')[1]
    #sss=[w.page_content for w in www]
    #print(sss)
