from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_react_agent
from langchain.agents.load_tools import load_tools
from langchain_community.tools.sql_database.tool import (BaseSQLDatabaseTool,
                                                         InfoSQLDatabaseTool,
                                                         ListSQLDatabaseTool,QuerySQLDataBaseTool)
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.agents import AgentAction
from langchain.agents.agent_types import AgentType
from langchain_core.prompts import PromptTemplate
from src.datasource import load_sqlitedb
from src.llm_models import google_models
from dotenv import load_dotenv

load_dotenv()
prompts=PromptTemplate(input_variables=['input','table_info','top_k'],template='''use the {input} to answer question on the {table_info} table. Get the {top_k} results'''
                                         )

#agentype=create_react_agent(llm=llm,tools=toolkits.get_tools())
def using_agent():
    db,tablenames,dbcontext=load_sqlitedb()
    model_llm="gpt2"#"google/flan-t4-xl"
    llm=HuggingFacePipeline.from_model_id(model_id=model_llm,task="text-generation")
    toolkits=SQLDatabaseToolkit(db=db,llm=llm)
    agent=create_sql_agent(llm=llm,toolkit=toolkits,agent_type='zero-shot-react-description'
                              )
    executor=AgentExecutor(agent=agent,tools=toolkits.get_tools())
    resp=executor.invoke({'input':'describe the schema of ActiveFluidModel table'})
    print(resp)

def using_chain():
    db,tablenames,dbcontext=load_sqlitedb()
    model_llm="gpt2"   
    #llm=HuggingFacePipeline.from_model_id(model_id=model_llm,task="text-generation")
    llm=google_models()
    #chain=SQLDatabaseChain.from_llm(llm=llm,db=db)
    #resp=chain.invoke("what is Joanna's surname")
    info= create_sql_query_chain(llm=llm,db=db)
    mes=db.run(info.invoke({'question':"what is Joanna's surname"}))
    #resp=info.invoke({'question':'number of columns in ActiveFluidModel table','table_info':'ActiveFluidModel','top_k':1})
    print(mes)


if __name__=="__main__":
    #using_agent()
    using_chain()

