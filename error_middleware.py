# error_middleware.py
import logging
from django.utils.deprecation import MiddlewareMixin

from ERRORS import send_error_to_telegram # type: ignore


class ErrorReportingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        error_message = f"Error occurred: {str(exception)}"
        logging.error(error_message)  # Log the error
        send_error_to_telegram(error_message)  # Send the error to Telegram
        return None  # Optionally, return a response or None
