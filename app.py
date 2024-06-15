import streamlit as st

from load import rag_chain


def qa_function(question):
    return rag_chain.invoke(question)


st.title("Plataforma de Preguntas y Respuestas")
st.write(
    "Ingresa tu pregunta en el cuadro de texto a continuación y obtén una respuesta:"
)

user_question = st.text_input("Pregunta:")

if st.button("Enviar"):
    if user_question:
        answer = qa_function(user_question)
        st.write("Respuesta:", answer)
    else:
        st.write("Por favor, ingresa una pregunta.")
