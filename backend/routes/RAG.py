from functools import wraps
from utils.validator import run_validator
from utils.formatter import run_formatter
import logging

log = logging.getLogger(__name__)

class RAG:
    def __init__(self):
        pass

    def _get_ai_response(self,request,query):
        def decorator(f):
            @wraps(f)
            def wrapper(request,query):
                
                return {}
            return wrapper
        return decorator


