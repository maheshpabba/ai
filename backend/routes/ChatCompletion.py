from functools import wraps
from utils.validator import run_validator
from utils.generator import run_executor_without_stream,run_executor_with_stream
from utils.formatter import run_formatter
import logging
from fastapi.responses import StreamingResponse

log = logging.getLogger(__name__)

class ChatCompletion:
    def __init__(self):
        pass

    def _get_ai_response(self,request,query):
        def decorator(f):
            @wraps(f)
            def wrapper(request,query):
                # input_prompt=run_validator(query)
                if query.stream:
                    log.debug('Stream Enabled')
                else:
                    log.debug('Stream Disabled')
                    # execution_result=run_executor_without_stream(input_prompt,llama_proxy,query)
                    # result= run_formatter(execution_result)
                    # return result
            return wrapper
        return decorator


