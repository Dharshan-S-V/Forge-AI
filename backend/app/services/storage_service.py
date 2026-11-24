"""
ForgeAI Storage Service.

Handles interactions with Supabase Storage.
"""

import uuid

from app.core.logging import get_logger
from app.db.supabase import get_supabase_admin_client

logger = get_logger(__name__)


class StorageService:
    """Service for managing files in Supabase Storage."""

    BUCKET_NAME = "documents"

    @classmethod
    def upload_file(cls, user_id: uuid.UUID, file_bytes: bytes, filename: str) -> str:
        """Upload a file to Supabase Storage.

        Args:
            user_id: The ID of the user uploading the file.
            file_bytes: The file contents.
            filename: Original or sanitized filename.

        Returns:
            The storage path of the uploaded file.
        """
        supabase = get_supabase_admin_client()
        
        # Path format: {user_id}/{uuid}-{filename}
        # Using a UUID prefix prevents collisions
        unique_prefix = str(uuid.uuid4())[:8]
        storage_path = f"{user_id}/{unique_prefix}-{filename}"

        logger.info(f"Uploading file to bucket {cls.BUCKET_NAME} at {storage_path}")

        result = supabase.storage.from_(cls.BUCKET_NAME).upload(
            file=file_bytes,
            path=storage_path,
            file_options={"upsert": "false"}
        )

        logger.info("File uploaded successfully", path=storage_path)
        return storage_path

    @classmethod
    def delete_file(cls, storage_path: str) -> None:
        """Delete a file from Supabase Storage."""
        supabase = get_supabase_admin_client()
        logger.info(f"Deleting file from bucket {cls.BUCKET_NAME}", path=storage_path)
        supabase.storage.from_(cls.BUCKET_NAME).remove([storage_path])
