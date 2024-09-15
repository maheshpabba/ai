from transformers import AutoTokenizer,TextStreamer,LlamaForCausalLM
from intel_extension_for_transformers.transformers import AutoModelForCausalLM,RtnConfig
from intel_extension_for_transformers.transformers.pipeline import pipeline
from langchain_community.llms import HuggingFacePipeline
model_name = "./models/hf-frompretrained-download/Llama-2-13b-chat-hf/"     
prompt = "Tell me joke"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
streamer = TextStreamer(tokenizer)
inputs = tokenizer(prompt, return_tensors="pt").input_ids


generate_kwargs={
        "do_sample":True,
        "top_k":40,
        "top_p":0.95,
        "num_beams":1,
        "temperature":0.95,
        "max_new_tokens":250,
        }

woq_config = RtnConfig(bits=4,weight_dtype="int4",compute_dtype="int8")

model = LlamaForCausalLM.from_pretrained(model_name,quantization_config=woq_config,verbose=True)
pipe=pipeline("text-generation",
model=model,tokenizer=tokenizer,framework="pt",**generate_kwargs)
llm=HuggingFacePipeline(pipeline=pipe)
# print(dir(pipe))
import time
st = time.time()
outputs=llm(prompt)
# outputs = model.generate(inputs,streamer=streamer,**generate_kwargs)
end = time.time()
output=tokenizer.batch_decode(outputs, skip_special_tokens=True)
print('-'*20, 'Output', '-'*20)
print(f'Inference time: {end-st} s')
print('-'*20, 'Output', '-'*20)
