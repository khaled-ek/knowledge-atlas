
import uuid

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.source import Chunk


class ChunkRepository:

    @staticmethod
    def create_chunks(
        db:Session,
        source_id: uuid.UUID,
        chunks: list,
        embeddings: list[list[float]]
    ) -> list[Chunk]:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings"
            )


        chunk_records = []

        for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
        ):
            chunk_record = Chunk(
                source_id=source_id,
                chunk_index=index,
                content=chunk.page_content,
                page_number=chunk.metadata.get("page_number"),
                metadata=chunk.metadata,
                embedding=embedding
            )

            chunk_records.append(chunk_record)

            db.add_all(chunk_records)
            db.commit()

            return chunk_records

    @staticmethod
    def delete_chunks_by_source_id(
        db:Session,
        source_id: uuid.UUID
    ) -> None:

        statement = delete(Chunk).where(
            Chunk.source_id == source_id
        )

        db.execute(statement)
        db.commit()