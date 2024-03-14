import json

import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from htmlTemplates import css, bot_template, user_template
from prompt import get_qa_prompt_template
from icecream import ic


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    qa_prompt = get_qa_prompt_template()
    ic(qa_prompt)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    with st.sidebar:
        with open("lang.json", "r", encoding="utf-8") as f:
            language_options = json.load(f)
        language = st.selectbox(
            language_options["English"]["language_text"], list(language_options.keys())
        )
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    st.header(
        language_options[language]["header"],
    )
    user_question = st.text_input(language_options[language]["user_question_text"])
    if user_question:
        try:
            handle_userinput(user_question)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    with st.sidebar:
        st.subheader(language_options[language]["document_header"])
        pdf_docs = st.file_uploader(
            language_options[language]["upload_button_text"],
            type="pdf",
            accept_multiple_files=True,
        )
        if st.button(language_options[language]["process_button_text"]):
            if pdf_docs:
                try:
                    with st.spinner(language_options[language]["processing_message"]):

                        raw_text = get_pdf_text(pdf_docs)

                        text_chunks = get_text_chunks(raw_text)

                        vectorstore = get_vectorstore(text_chunks)

                        st.session_state.conversation = get_conversation_chain(
                            vectorstore
                        )
                    st.success(language_options[language]["success_message"], icon="🎉")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.error(language_options[language]["error_message"], icon="🚨")


if __name__ == "__main__":
    main()
