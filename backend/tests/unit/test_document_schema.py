"""
Regression test for app.schemas.document.DocumentResponse.

Covers Issue #7: the Document ORM model exposes the `metadata` DB column
via the Python attribute `doc_metadata`. DocumentResponse.metadata must
read from that attribute via validation_alias, not silently default to {}.
"""

from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.document import DocumentResponse


class _FakeDocumentORM:
    """Minimal stand-in for the SQLAlchemy Document model's public
    attributes, without requiring a live database.
    """

    def __init__(self, doc_metadata: dict):
        self.id = uuid4()
        self.filename = "report.pdf"
        self.original_filename = "Report.pdf"
        self.file_type = "pdf"
        self.file_size = 1024
        self.status = "completed"
        self.chunk_count = 5
        self.doc_metadata = doc_metadata
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)


def test_document_response_reads_real_metadata_from_orm_attribute():
    orm_obj = _FakeDocumentORM(doc_metadata={"source": "pipeline", "index": 2})

    response = DocumentResponse.model_validate(orm_obj)

    assert response.metadata == {"source": "pipeline", "index": 2}


def test_document_response_defaults_to_empty_dict_when_metadata_absent():
    orm_obj = _FakeDocumentORM(doc_metadata={})

    response = DocumentResponse.model_validate(orm_obj)

    assert response.metadata == {}


def test_document_response_still_accepts_metadata_by_public_name():
    """populate_by_name=True must still allow constructing directly from a
    dict using the public field name "metadata" (e.g. in other tests or
    direct API construction), not just via ORM attribute aliasing.
    """
    response = DocumentResponse(
        id=uuid4(),
        filename="a.txt",
        original_filename="A.txt",
        file_type="txt",
        file_size=10,
        status="uploaded",
        chunk_count=0,
        metadata={"foo": "bar"},
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    assert response.metadata == {"foo": "bar"}
