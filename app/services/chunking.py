
#from langchain_docling import DoclingLoader
#from langchain_docling.loader import ExportType
#from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# 1. Load and convert the PDF to clean Markdown using Docling

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkingService:

    @staticmethod
    def chunk_document (filepath: str, source_id: str):

        spliter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""]
        )

        loader = PyPDFLoader(filepath)
        docs = loader.load()

        chunks = spliter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["source_id"] = source_id

            # PyPDFLoader uses zero-based page numbers.
            # Convert to one-based page numbers for our database.
            if "page" in chunk.metadata:
                chunk.metadata["page_number"] = chunk.metadata["page"] + 1


        return chunks






