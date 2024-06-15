import os

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents.base import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FILE_PATH = os.getenv("FILE_PATH")


def load_pdf(file_path: str) -> list[Document]:
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages


embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)

vectorstore = Chroma.from_documents(
    documents=load_pdf(FILE_PATH), embedding=embeddings_model
)

retriever = vectorstore.as_retriever()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


template = """
Eres un bot maestro que enseña a los niños sobre cuentos usando el siguiente contexto
para responder a la pregunta lo más detallado posible.
Contexto: {context}
Question: {question}
Respuesta:
"""

prompt = PromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
