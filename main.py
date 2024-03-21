import streamlit as st
import time
from src.sourcefiles import analyse_documents
st.title('Document Analyser')
with st.sidebar:
    st.sidebar.file_uploader('get file path by copying')
    path=''
    path= st.text_area('Enter file path',placeholder="file name")
    st.write(path)

with st.form('chat_form'):
    query = st.text_area('Enter your query below :question:','summarise the uploaded document!')
    submitted = st.form_submit_button(':blue[Submit Request] :running:')
    if submitted:
        with st.spinner('please wait ...:raised_hand_with_fingers_splayed:'):
            starttime=time.time()
            chain=analyse_documents(path)
            res=chain.invoke(query)
            endtime=time.time()
            st.write(f' the inference ran for {round((endtime-starttime),2)} seconds')
            st.info(res)