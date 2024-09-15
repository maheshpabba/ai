from functools import wraps
from utils.validator import run_validator
from utils.generator import run_executor_without_stream,run_executor_with_stream
from utils.formatter import run_formatter
import logging
from fastapi.responses import StreamingResponse

log = logging.getLogger(__name__)


class FileUploader:
    def __init__(self):
        pass

    def _upload(self,request,file):
        def decorator(f):
            @wraps(f)
            def wrapper(request,file):
                pass
            return wrapper
        return decorator


