from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.LLMClass import TransformersLLM
from langchain.chains import LLMChain
from langchain_core.runnables import Runnable
from tools.prompts import Llama2EmptyPromptWithoutRole,Llama3EmptyPromptWithoutRole
from langchain_core.prompts import PromptTemplate
from gptcache import Cache
from gptcache.manager.factory import manager_factory
from gptcache.processor.pre import get_prompt
from langchain.cache import GPTCache
from utils.LLMClass import TransformersLLM
import hashlib
import langchain
import logging

log = logging.getLogger(__name__)



# def get_hashed_name(name):
#     return hashlib.sha256(name.encode()).hexdigest()


# get the content(only question) form the prompt to cache
# def get_msg_func(data, **_):
#     return data.get("prompt")[-1].content

# def init_gptcache(cache_obj: Cache, llm: str):
#     hashed_llm = get_hashed_name(llm)
#     cache_obj.init(
#         pre_embedding_func=get_msg_func,
#         data_manager=manager_factory(manager="map", data_dir=f"map_cache_{hashed_llm}"),
#     )


class LLMLoader:
    def __init__(self):
        self.callback=StreamingStdOutCallbackHandler()
        self.init_llm()
        
    def __call__(self):
        # return self.LLAMA2,self.LLAMA3,self.CODELLAMA
        return self.LLAMA2


    def init_llm(self):
        # self.LLAMA2=TransformersLLM(self.model_name,callbacks=([self.callback]))
        # print('Model Loaded')
        # return self.LLM
        self.LLAMA2=self.get_chatllm2()
        # self.LLAMA3=self.get_chatllm3()
        # self.CODELLAMA=self.get_codellm()

    def get_chatllm2(self):
        model_name = "/gesdcllm/models/models/hf-frompretrained-download/Llama-2-13b-chat-hf"
        # gguf_file="llama-2-7b-function-calling.Q3_K_M.gguf"
        callback=StreamingStdOutCallbackHandler()
        LLM=TransformersLLM(model_name,callbacks=[callback])
        # LLM=TransformersLLM(model_name)
        prompt=PromptTemplate(template=Llama2EmptyPromptWithoutRole,input_variables=["query"])
        llmchain: Runnable = prompt | LLM 
        result=llmchain.invoke('what is solar system?')
        # llm=LLMChain(llm=LLM,prompt=prompt)
        # result=llmchain.run('Tell me a Joke')
        log.info(result)
        return LLM


    def get_chatllm3(self):
        model_name = "/gesdcllm/models/models/hf-frompretrained-download/Llama-3-8b-chat-hf/"
        callback=StreamingStdOutCallbackHandler()
        LLM=TransformersLLM(model_name,callbacks=[callback])
        # LLM=TransformersLLM(model_name)
        prompt=PromptTemplate(template=Llama3EmptyPromptWithoutRole,input_variables=["query"])
        log.debug(prompt)
        llmchain=LLMChain(llm=LLM,prompt=prompt)
        result=llmchain.run('tell me a joke')
        log.info(result)
        return LLM


    def get_codellm(self):
        model_name = "/gesdcllm/models/models/hf-frompretrained-download/CodeLlama-7b-hf/"
        callback=StreamingStdOutCallbackHandler()
        LLM=TransformersLLM(model_name,callbacks=[callback])
        # LLM=TransformersLLM(model_name)
        prompt=PromptTemplate(template=Llama2EmptyPromptWithoutRole,input_variables=["query"])
        llmchain=LLMChain(llm=LLM,prompt=prompt)
        result=llmchain.run('tell me a joke')
        log.info(result)
        return LLM



# langchain.llm_cache = GPTCache(init_gptcache)
