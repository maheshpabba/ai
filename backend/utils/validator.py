from tools.prompts import *
from conf.models import ApiResponse
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
import logging
log = logging.getLogger(__name__)


class Validator:
    def __init__(self,prompt):
        self.prompt=prompt
        # log.debug('Inputs i received: %s',self.prompt)
        self.modeldict={
            "llama2":{
                "EmptyPromptWithRole":Llama2EmptyPromptWithRole,
                "EmptyPromptWithoutRole":Llama2EmptyPromptWithoutRole,
                "DefaultPrompt":DefaultLlama2Prompt
            },
            "llama3":{"EmptyPromptWithRole":Llama3EmptyPromptWithRole,
                "EmptyPromptWithoutRole":Llama3EmptyPromptWithoutRole,
                "DefaultPrompt":DefaultLlama3Prompt},
            "codellama":{}
        }
        

    def _run(self):
        parser = PydanticOutputParser(pydantic_object=ApiResponse)

        if self.prompt.roleContent is not None and len(self.prompt.roleContent) > 0:
            if self.prompt.stream:
                self.input_prompt=PromptTemplate(
                    template=self.modeldict[self.prompt.model]['EmptyPromptWithRole'],
                    input_variables=["query"],
                    )
                # self.input=self.input_prompt.format(query=self.prompt.userMessage,systemrole=self.prompt.roleContent)
            else:
                self.input_prompt=PromptTemplate(
                    template=self.modeldict[self.prompt.model]['DefaultPrompt'],
                    input_variables=["query"],
                    partial_variables={"format_instructions":parser.get_format_instructions()}
                )
                # self.input=self.input_prompt.format(query=self.prompt.userMessage,systemrole=self.prompt.roleContent)

        elif (self.prompt.roleContent is None and len(self.prompt.roleContent) == 0):

            if self.prompt.stream:
                self.input_prompt=PromptTemplate(
                    template=self.modeldict[self.prompt.model]['EmptyPromptWithoutRole'],
                    input_variables=["query"],
                    )
                # self.input=self.input_prompt.format(query=self.prompt.userMessage)
            else:
                self.input_prompt = PromptTemplate(
                        template=self.modeldict[self.prompt.model]['DefaultPrompt'],
                        input_variables=["query"],
                        partial_variables={"format_instructions":parser.get_format_instructions()}
                        )
                # self.input=self.input_prompt.format(query=self.prompt.userMessage)
        else:
            self.input_prompt=PromptTemplate(
                    template=self.modeldict[self.prompt.model]['EmptyPromptWithoutRole'],
                    input_variables=["query"],
                    )
            # self.input=self.input_prompt.format(query=self.prompt.userMessage)

        return self.input_prompt
        
            
def run_validator(prompt):
    return Validator(prompt)._run()