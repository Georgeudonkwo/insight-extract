import streamlit as st
import time
from src.sourcefiles import analyse_documents,load_wiki
st.title('Document Analyser')
cols=st.columns([0.4,0.6])
doc=None
with st.sidebar:
    path=''
    st.sidebar.selectbox('INPUT MODE',['files','search'],key='select')
    if st.session_state.select=='files':
        st.sidebar.file_uploader('get file path by copying')
        path= st.text_area('Enter file path',placeholder="file name")
        st.write(path)
    elif st.session_state.select=='search':
        path= st.text_area('Enter search token',placeholder="Search")
        st.write(path)
if st.session_state.select=='files':
    spintext='Loading and analysing document, please wait ...:raised_hand_with_fingers_splayed:'
else:
    spintext='searching wikipedia. This may take some time ...:raised_hand_with_fingers_splayed:'

with st.form('chat_form'):
    with cols[0]:
        st.header(':red[Insight Extraction]')
    query = st.text_area('What do you want to do :question:','summarise the uploaded document!')
    submitted = st.form_submit_button(':blue[Submit Request] :running:')
    if submitted:
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
                if st.session_state.select=='search':
                    text=doc
                else:
                    text="".join([d.page_content for d in doc])
                st.write(text)