import logging

from django.db import transaction

logger = logging.getLogger(__name__)


def schedule_file_deletion(field_file):
    if not field_file or not field_file.name:
        return

    file_name = field_file.name
    storage = field_file.storage

    def delete_file():
        try:
            storage.delete(file_name)
        except Exception:
            logger.exception(
                "Failed to delete file: %s",
                file_name,
            )

    transaction.on_commit(delete_file)
