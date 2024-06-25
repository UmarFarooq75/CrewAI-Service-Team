from PyPDF2 import PdfReader
from crewai_tools import tool
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class SearchTool:
    @staticmethod
    @tool("searchfromtext")
    def search_from_text(query: str, text: list[str]) -> list[str]:
        """Use this tool to search from extracted text."""
        text_chunks = SearchTool.get_text_chunks(text)
        vectorstore = SearchTool.get_vectorstore_from_chunks(text_chunks)
        conversation_chain = SearchTool.get_conversation_chain(vectorstore)
        response = conversation_chain({"question": query})
        return response

    @staticmethod
    def get_vectorstore_from_chunks(text: str, model="text-embedding-3-small"):
        text = text.replace("\n", " ").replace("\n\n", " ").replace(" \n", " ").replace("\n ", " ")
        embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
        return embedding

    @staticmethod
    def get_conversation_chain(vectorstore):
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain

    @staticmethod
    def get_text_chunks(text: str, chunk_size=1000, chunk_overlap=200):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    @staticmethod
    def get_pdf_text(file_path="E:/GenAI/serviceteam/src/serviceteam/tools/Overview.pdf") -> str:
        if not os.path.exists(file_path):
            return f"Error: The file at {file_path} does not exist."

        try:
            text = ""
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"An error occurred while reading the PDF: {e}"
