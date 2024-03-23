from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.language_models.base import BaseLanguageModel
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from src.llm_models import google_models

def db_instance(connString:str):
    db=SQLDatabase.from_uri(connString)
    table_names=db.get_usable_table_names()
    table_info=db.get_table_info()
    context=db.get_context()
    return db,table_info,table_names,context

def fetch(connString:str,llm:BaseLanguageModel):
    db,tbl_info,tbl_names,contxt=db_instance(connString=connString)
    sqlprompt=PromptTemplate.from_template(template='''you are an expert database administrator,
                                          use the provided: {input} to generate good
                                          sql query for the database dialet: {dialet}
                                          using the schema {table_info}
                                           return {top_k} results''')
    sssss=create_sql_query_chain(llm=llm,db=db,prompt=sqlprompt)
    ch=(sssss|StrOutputParser())
    

    res=ch.invoke({'question':'what is Joanna surname','dialet':db.dialect,'table_info':tbl_names,
                      'top_k':5})
    res=db.run('SELECT SurName FROM Person WHERE Firstname ="JOANNA"')
    #prompt=PromptTemplate(input_types=['query'],
                          #template='use the query,{query}: to get data from the database')

    #chain=(RunnablePassthrough().assign(dialet=db.dialect,table_info=tbl_info,top_k=5)
          # |sqlprompt
           #|llm
           #|StrOutputParser()
          # )
    return res

if __name__=='__main__':
    llm=google_models()
    connstr=R"sqlite:///C:\Users\eno.udonkwo\Desktop\2024 works\data\misc.db"
    ch=fetch(connString=connstr,llm=llm)
    print(ch)#.invoke({'input':"what is Joanna's surname"}))