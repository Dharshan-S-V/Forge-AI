"""
Regression tests for the chat API response schemas.

Covers Issue #4: api/v1/chat.py previously defined local Pydantic models
without from_attributes=True and returned raw SQLAlchemy ORM objects
against them, which raised ResponseValidationError on every request. The
fix routes responses through app.schemas.chat's BaseSchema-derived models
instead, which correctly set from_attributes=True.
"""

from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.chat import ChatMessageResponse, ChatSessionResponse


class _FakeChatSessionORM:
    def __init__(self):
        self.id = uuid4()
        self.title = "New Chat"
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)


class _FakeChatMessageORM:
    def __init__(self):
        self.id = uuid4()
        self.role = "assistant"
        self.content = "Hello, how can I help?"
        self.sources = [{"id": 1, "filename": "doc.pdf"}]
        self.created_at = datetime.now(timezone.utc)


def test_chat_session_response_validates_from_orm_object():
    """This is exactly what api/v1/chat.py's create_chat/list_chats/get_chat
    routes do: return a raw ORM object against this response_model. Must
    not raise.
    """
    orm_obj = _FakeChatSessionORM()

    response = ChatSessionResponse.model_validate(orm_obj)

    assert response.id == orm_obj.id
    assert response.title == "New Chat"


def test_chat_message_response_validates_from_orm_object():
    """This is exactly what send_message returns against ChatMessageResponse."""
    orm_obj = _FakeChatMessageORM()

    response = ChatMessageResponse.model_validate(orm_obj)

    assert response.role == "assistant"
    assert response.content == "Hello, how can I help?"
    assert response.sources == [{"id": 1, "filename": "doc.pdf"}]
