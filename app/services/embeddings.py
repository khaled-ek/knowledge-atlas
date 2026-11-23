
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings

class EmbeddingService:

    def __init__(self):
        self.model = OpenAIEmbeddings(
            model= settings.EMBEDDING_MODEL,
            api_key= settings.OPEN_API_KEY,
        )

    def embed_text(self, text: str) -> list[float]:
        return self.model.embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.embed_documents(texts)


