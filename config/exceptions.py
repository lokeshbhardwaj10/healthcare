import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Uniform error responses; DB integrity errors become 400s instead of 500s."""
    response = exception_handler(exc, context)

    if response is None and isinstance(exc, IntegrityError):
        logger.warning("IntegrityError: %s", exc)
        return Response(
            {"detail": "Database integrity error. The record may already exist."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return response
