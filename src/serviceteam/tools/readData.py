from PyPDF2 import PdfReader
from crewai_tools import tool
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class DocsData:
    @staticmethod
    @tool("queryHandler")
    def get_data_from_pdf() -> str:
        """Use this tool to read data from PDFs and return the extracted text."""
        text = DocsData.get_pdf_text()
        return text
    
    @staticmethod
    def get_pdf_text():
        text = ""
        file_path = "E:/GenAI/serviceteam/src/serviceteam/tools/Overview.pdf"
        
        if not os.path.exists(file_path):
            return f"Error: The file at {file_path} does not exist."

        try:
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"An error occurred while reading the PDF: {e}"
