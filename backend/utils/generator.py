from langchain.chains import LLMChain
import logging
from langchain_core.runnables import Runnable

log = logging.getLogger(__name__)

class Executor:
    def __init__(self,prompt,model,params):
        self.prompt=prompt
        self.params=params
        self.query=self.params.userMessage
        self.LLM=model
        self.LLM.max_new_tokens=self.params.max_new_tokens
        self.LLM.top_p=self.params.top_p
        self.LLM.top_k=self.params.top_k
        self.LLM.max_new_tokens=self.params.max_new_tokens
        self.LLM.temperature=self.params.temperature
        
    def _run(self):
        # response,input_tokens,response_tokens=self.LLM(self.prompt)
        # log.debug(f"input_tokens: {input_tokens}")
        # log.debug(f"response_tokens: {response_tokens}")

        # self.llmchain=LLMChain(llm=self.LLM,prompt=self.prompt)
        # return self.llmchain.run(self.query)

        self.llmchain: Runnable = self.prompt | self.LLM
        return self.llmchain.invoke(self.query)

    def _stream(self):
        # self.llmchain=LLMChain(llm=self.LLM,prompt=self.prompt)
        # return self.llmchain.astream(self.query)

        self.llmchain: Runnable = self.prompt | self.LLM
        return self.llmchain.astream(self.query)
        
def run_executor_without_stream(prompt,model,params):
    return Executor(prompt,model,params)._run()

def run_executor_with_stream(prompt,model,params):
    return Executor(prompt,model,params)._stream()

