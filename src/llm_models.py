from langchain_anthropic import Anthropic,ChatAnthropic,ChatAnthropicMessages
from langchain_openai import ChatOpenAI,OpenAI,OpenAIEmbeddings
from langchain_google_genai import (GoogleGenerativeAI,GoogleGenerativeAIEmbeddings,
                                    ChatGoogleGenerativeAI,GoogleVectorStore)
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.embeddings.huggingface import HuggingFaceInstructEmbeddings

from dotenv import load_dotenv
load_dotenv('.env')

def anthropic_models(model_id:str='claude-3-opus-20240229'):
    model=ChatAnthropic(model_name=model_id)
    return model

def Hf_models(*,model_id:str='gpt2',task='text-generation'):
    model=HuggingFacePipeline.from_model_id(model_id=model_id,task=task)
    return model
def google_models(model_id='gemini-pro'):
    model=GoogleGenerativeAI(model=model_id, temperature=0.0)
    return model
def openai_models(model_id='gpt-3.5-turbo'):
    model=ChatOpenAI(model=model_id)
    return model
def openai_embeddings(model_id='gpt-3.5-turbo'):
    model=openai_embeddings(model=model_id)
    return model
def google_embedding(model_id='models/embedding-001'):
    embedings=GoogleGenerativeAIEmbeddings(model=model_id)
    return embedings
def Hf_embeddings(model_id='hkunlp/instructor-large'):
    embedings=HuggingFaceInstructEmbeddings(model_name = model_id)
    return embedings
if __name__=="__main__":
   # model=Hf_models()
    #res=model.invoke("discuss climate change,and mitigating measures")
    res=Hf_embeddings().embed_query('my name is george udonkwo')
    print(res)
