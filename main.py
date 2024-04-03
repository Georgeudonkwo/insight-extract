import streamlit as st
import time
from src.sourcefiles import analyse_documents,load_wiki
from src.fetch import fetch_agent
from src.llm_models import google_models
st.title('Document Analyser')
cols=st.columns([0.4,0.6])
doc=None
llm=None
database_object=None
with st.sidebar:
    path=''
    st.sidebar.selectbox('Data Context',['files','Database','wikipedia'],key='select')
    if st.session_state.select=='files':
        st.sidebar.file_uploader('get file path by copying')
        path= st.text_area('Enter file path',placeholder="file name")
        st.write(path)
    elif st.session_state.select=='wikipedia':
        path= st.text_area('Enter search token',placeholder="Search wikipedia")
        st.write(path)
    elif st.session_state.select=='Database':
        llm=google_models()
        st.sidebar.selectbox('db type',['sqlite','mysql','mssql'],key='db_type')

        dialet=st.session_state.db_type# st.text_input("Database Type",value='mysql')
        if dialet.strip()=='mysql':
            engine=st.text_input('dialet',value='mysqlconnector')
            user=st.text_input('user',value='George')
            password=st.text_input('password',value='georgedb*george1')
            host=st.text_input('host',value='CCLNG-PC310')
            port=st.text_input('port',value=3306)
            db_name=st.text_input('database name',value='MISC')
            connstr=f"{dialet}+{engine}://{user}:{password}@{host}:{port}/{db_name}"
            st.write(connstr)
        elif  dialet.strip()=='sqlite':
            st.sidebar.file_uploader('get file path by copying')
            filepath=st.text_area('dialet',value=R'C:\Users\eno.udonkwo\Desktop\2024 works\data\PVTRMS-mod.db')
            connstr=R"sqlite:///"+f"{filepath.strip('"')}"
            st.write(connstr)
        elif dialet.strip()=='mssql':
            dialet=st.text_input("Database Type",value='sqlite')
            filepath=st.text_area('file path',value=R"C:\Users\eno.udonkwo\Desktop\2024 works\data\misc.db")
            connstr=f"{dialet}:///"+filepath
        
            


        
if st.session_state.select=='files':
    spintext='Loading and analysing document, please wait ...:raised_hand_with_fingers_splayed:'
else:
    spintext='searching wikipedia. This may take some time ...:raised_hand_with_fingers_splayed:'

with st.form('chat_form'):
    with cols[0]:
        st.header(':red[Insight Extraction]')
    if st.session_state.select=='files'or st.session_state.select=='wikipedia':
        query = st.text_area('What do you want to do :question:','summarise the uploaded document!')
    elif st.session_state.select=='Database':
        query=st.text_area('interact with your database',value='fetch table info')
    submitted = st.form_submit_button(':blue[Submit Request] :running:')
    if submitted:
        if st.session_state.select=='files' or st.session_state.select=='wikipedia':
            with st.spinner(spintext):
                starttime=time.time()
                chain,doc=analyse_documents(path)
                res=chain.invoke(query)
                endtime=time.time()
                st.write(f' the inference ran for {round((endtime-starttime),2)} seconds')
                st.info(res)
            with cols[1]:
                with st.expander(':green[SEE SOURCE DOCUMENT]'):
                    st.header('Source')
                    if st.session_state.select=='wikipedia':
                        text=doc
                    else:
                        text="".join([d.page_content for d in doc])
                    st.write(text)
        elif st.session_state.select=='Database':
            spintext='connecting to the database, this may take awhile. please wait ...:raised_hand_with_fingers_splayed:'
            with st.spinner(spintext):
                starttime=time.time()
                database_object,tbl_info,tbl_names,contxt=fetch_agent(connString=connstr,llm=llm,query=query)
                endtime=time.time()
                st.write(f' the inference ran for {round((endtime-starttime),2)} seconds')
                st.info(database_object)
            with cols[1]:
                with st.expander('See database tables'):
                    #st.write(tbl_names)
                    #st.write(tbl_info)
                    #print("")
                    st.write(contxt)