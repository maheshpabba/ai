from transformers import AutoTokenizer,TextStreamer,TextIteratorStreamer,LlamaTokenizer
from intel_extension_for_transformers.transformers import AutoModelForCausalLM,RtnConfig
from intel_extension_for_transformers.transformers.pipeline import pipeline
from langchain.schema import BaseOutputParser,LLMResult
from langchain.llms.base import LLM
from langchain_community.llms.utils import enforce_stop_tokens
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from functools import partial
from threading import Thread
from pydantic import BaseModel, Field, validator
from typing import List, Mapping, Optional, Any, Dict
# from neural_speed import Model
import threading
import re
import datetime
# import tiktoken
import logging
import time
import torch
import asyncio
# import sys


log = logging.getLogger(__name__)

class ReturnValueThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result


# class EosListStoppingCriteria(StoppingCriteria):
#     def __init__(self, eos_sequence=[2277, 29937]):
#         self.eos_sequence = eos_sequence

#     def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
#         last_ids = input_ids[:,-len(self.eos_sequence):].tolist()
#         return self.eos_sequence in last_ids




class TransformersLLM(LLM):

    model_folder_path: str = Field(None, alias='model_folder_path')
    model_name: str = Field(None, alias='model_name')
    gguf_file: str = Field(None, alias='gguf_file')
    # backend: Optional[str] = 'llama'
    temperature: Optional[float] = 0.75
    top_p: Optional[float] = 0.5
    top_k: Optional[int] = 40
    max_new_tokens: Optional[int] = 200
    repetition_penalty: Optional[float] = 1.15
    threads: Optional[int] = 20 #old value 40
    # batch_size: Optional[int] = 32
    ctx_size: Optional[int] = 4096
    use_cache: bool = True
    # max_request_num: Optional[int] = 3
    # stop_token_id: Any = None
    stop_token: Any = None
    model: Any = None
    tokenizer: Any = None
    ignore_prompt: bool = True
    continuous_batching: bool = True
    num_return_sequences: Optional[int] = 1
    do_sample: bool = False
    # woq_config: Optional[Dict] = None
    #########

    def __init__(self, model_folder_path, gguf_file=None,callbacks=None, **kwargs):
        super(TransformersLLM, self).__init__()
        self.model_folder_path: str = model_folder_path
        self.gguf_file = gguf_file
        self.callbacks = callbacks
        self.tokenizer=AutoTokenizer.from_pretrained(self.model_folder_path, trust_remote_code=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        # self.stop_token = "<|eot_id|>"
        # self.stop_token_id = self.tokenizer.encode(self.stop_token)[0]
        # self.tokenizer.pad_token = self.stop_token
        # self.model=Model()
        # self.model.init(self.model_folder_path, use_quant=True,weight_dtype="int4", compute_dtype="int8")
        # self.model.batch_size=32
        # self.woq_config = RtnConfig(bits=8,weight_dtype="int4", compute_dtype="int8",tokenizer=self.tokenizer)
        # self.model=AutoModelForCausalLM.from_pretrained(self.model_folder_path,quantization_config=self.woq_config,verbose=None)
        self.model=AutoModelForCausalLM.from_pretrained(self.model_folder_path, load_in_4bit=True,load_from_File=True,gguf_file=self.gguf_file)
        self.model.batch_size=32
        # self.generator=pipeline('text-generation',self.model_folder_path)
        #########


    @property
    def _get_model_default_parameters(self):
        return {
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "repetition_penalty" : self.repetition_penalty,
            "threads": self.threads,
            "continuous_batching": self.continuous_batching,
            "do_sample": self.do_sample,
            "ctx_size": self.ctx_size,
            "ignore_prompt": self.ignore_prompt,
            "num_return_sequences": self.num_return_sequences,
            "top_p":self.top_p,
            "top_k":self.top_k,
            "ignore_prompt":self.ignore_prompt,
            "use_cache":self.use_cache
            # "eos_token_id":self.stop_token_id
            # "max_request_num":3,
            # "batch_size":self.batch_size

        }

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            'model_name': self.model_name,
            'model_path': self.model_folder_path,
            'model_parameters': self._get_model_default_parameters
        }

    @property
    def _llm_type(self) -> str:
        return 'llama'



    async def _acall(self,
              prompt: str,
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              stream=True,
              job_done=None,
              **kwargs) -> str:
        start_time=datetime.datetime.now()
        params = {
            **self._get_model_default_parameters,
            **kwargs
        }
        log.info(params)
        text_callback = None
        if run_manager:
            text_callback = partial(run_manager.on_llm_new_token, verbose=self.verbose)

        input_ids = self.tokenizer(prompt, max_length=4096, return_tensors='pt',truncation=True,padding=True).input_ids
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        generate_kwargs = dict(input_ids=input_ids,
                                # max_new_tokens=params['max_new_tokens'],
                                # temperature=params['temperature'],
                                # repetition_penalty=params['repetition_penalty'],
                                # do_sample=False,
                                streamer=streamer,
                                **params
                                )
        with torch.no_grad():
            t = Thread(target=self.model.generate, kwargs=generate_kwargs)
            start_time=time.time()
            t.start()
            response = ""
            output_word_len = len(response)
            time_to_first_token=time.time()-start_time
            log.info('Time to First Token: %s',time_to_first_token)
            first_word_output_time = datetime.datetime.now()
            for i, new_text in enumerate(streamer):
                if len(new_text) == 0:
                    continue
                if output_word_len == 0:
                    first_word_output_time = datetime.datetime.now()
                if new_text is not None:
                    await text_callback(new_text)
                    await asyncio.sleep(0.01)
                    response += new_text
                    output_word_len += 1
                if response.endswith(new_text * 5) and (new_text != ""):
                    break
            end_time=datetime.datetime.now()
            time.sleep(0.1)
            duration = int((end_time - start_time).total_seconds() * 1000)
            first_token_latency = int(
                (first_word_output_time - start_time).total_seconds() * 1000 * 3/4
            )
            msecond_per_token = (
            duration  / (output_token_len - input_token_len)
            if output_token_len != 1 else 0
                )
        # if stop:
        #     response = enforce_stop_tokens(response, stop)
        return response.strip()

    def _call(self,
              prompt: str,
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              stream=False,
              job_done=None,
              **kwargs) -> str:

        params = {
            **self._get_model_default_parameters,
            **kwargs
        }
        t_total=0
        total_new_tokens = 0
        text_callback = None
        if run_manager:
            text_callback = partial(run_manager.on_llm_new_token, verbose=self.verbose)

        input_ids = self.tokenizer(prompt, max_length=4096, return_tensors='pt',truncation=True,padding=True).input_ids
        prompt_length=input_ids.shape[1]
        log.info(f"Total Input Tokens: {prompt_length}")
        generate_kwargs = dict(input_ids=input_ids,
                                # max_new_tokens=params['max_tokens'],
                                # temperature=params['temperature'],
                                # repetition_penalty=params['repetition_penalty'],
                                # do_sample=False,
                                **params
                                )
        # self.pipeline=pipeline('text-generation',model=self.model,tokenizer=self.tokenizer,model_kwargs=generate_kwargs)
        with torch.no_grad():
            #This is another way of calling the thread and joining the results.
            # def inner():
            #     for text in streamer:
            #         yield text
            #     thread.join()

            # return inner()

            t=ReturnValueThread(target=self.model.generate,kwargs=generate_kwargs)
            t_b = time.time()
            t.start()
            outputs=t.join()
            log.debug(outputs)
            response=self.tokenizer.batch_decode(outputs,skip_special_tokens=True)[0]
            t_e = time.time()
            t_total += t_e - t_b
            total_new_tokens += len(outputs[0]) - input_ids.shape[-1]
            log.info(input_ids.shape[0])
            log.info(input_ids.shape[-1])
            log.info(f"Total New Tokens: {total_new_tokens}")
            log.info(f"Tokens Per Second:  {total_new_tokens / t_total}")
        # if stop:
        #     response = enforce_stop_tokens(response, stop)
        return str(response)


    def create_llm_result(
        self, choices: Any, prompts: List[str], token_usage: Dict[str, int]
    ) -> LLMResult:
        """Create the LLMResult from the choices and prompts."""
        generations = []
        for i, prompt in enumerate(prompts):
            sub_choices = choices
            generations.append(
                [
                    Generation(
                        text='\n\n' + choice["text"].strip().replace("<|im_end|>", ''),
                        generation_info=dict(
                            finish_reason=choice.get("finish_reason"),
                            logprobs=choice.get("logprobs"),
                        ),
                    )
                    for choice in sub_choices
                ]
            )
        return LLMResult(
            generations=generations, llm_output={"token_usage": token_usage}
        )
        

