from functools import wraps
from utils.validator import run_validator
from utils.generator import run_executor_without_stream,run_executor_with_stream
from utils.formatter import run_formatter
import logging
from fastapi.responses import StreamingResponse

log = logging.getLogger(__name__)


class Completion:
    def __init__(self):
        pass

    def _get_ai_response(self,request,body):
        def decorator(f):
            @wraps(f)
            def wrapper(request,body):
                log.debug(query)
                # log.debug(Request)
                # input_prompt=run_validator(query)
                # log.debug(input_prompt)
                if query.stream:
                    log.debug('Stream Enabled')
                    # streamer= run_executor_with_stream(input_prompt,llama_proxy,query)
                    # for chunk in streamer:
                    #     return StreamingResponse(chunk,media_type='text/event-stream')
                else:
                    log.debug('Stream Disabled')
                    # execution_result=run_executor_without_stream(input_prompt,llama_proxy,query)
                    # result= run_formatter(execution_result)
                    # return result
            return wrapper
        return decorator


