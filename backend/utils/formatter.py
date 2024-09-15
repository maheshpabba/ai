import json
import regex
import logging
from conf.models import ApiResponse
log = logging.getLogger(__name__)

class Formatter:
    def __init__(self,result):
        self.result=result
        # log.info(result)

    def _run(self):
        # start_pos=self.result.find('[/INST]') + len('[/INST]')
        # ch=self.result[start_pos:]
        # pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
        # data=pattern.findall(ch)
        # if not data:
        #     log.debug(self.result)
        #     return json.loads(self.result)
        # else:
        #     log.debug(data)
        #     return json.loads(data[0])
        return ApiResponse(**{'response':self.result,'response_type':'string'})

def run_formatter(result):
    return Formatter(result)._run()