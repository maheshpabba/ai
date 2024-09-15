DefaultLlama2Prompt="""
    <s>[INST] <<SYS>>
    you are an expert Datacenter Networking AI Assistant.\n{format_instructions}\n
    <</SYS>>

    {query} [/INST]
    """


Llama2PromptWithRAG="""
    <s>[INST] <<SYS>>
    you are an expert Datacenter Networking AI Assistant. 
    Given the Following Information: {retrieved_info} respond to user queries.\n{format_instructions}\n
    <</SYS>>
    {query} [/INST]
    """

Llama2EmptyPromptWithRole="""
    <s>[INST] <<SYS>>
        {systemrole}
    <</SYS>>
    {query} [/INST]
    """

Llama2EmptyPromptWithoutRole="""
    <s>[INST] <<SYS>>
    you are an expert Datacenter Networking AI Assistant.
    <</SYS>>
    {query} [/INST]
    """


Llama2PromptWithFunctions="""
    <s>[INST] <<SYS>>
    you are an expert Datacenter Networking AI Assistant. 
    Given the Following Information: {retrieved_info} respond to user queries.\n{format_instructions}\n
    <</SYS>>
    {query} [/INST]

"""


DefaultLlama3Prompt="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    you are an expert Datacenter Networking AI Assistant.\n{format_instructions}\n
    <|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    {query} <|eot_id|>
    """


Llama3PromptWithRAG="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    you are an expert Datacenter Networking AI Assistant. 
    Given the Following Information: {retrieved_info} respond to user queries.\n{format_instructions}\n
    <|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    {query} [/INST]
    """

Llama3EmptyPromptWithRole="""<|begin_of_text|>
    <|start_header_id|>system<|end_header_id|>
    {systemrole}
    <|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    {query}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

Llama3EmptyPromptWithoutRole="""<|begin_of_text|>
    <|start_header_id|>system<|end_header_id|>
    you are an expert Datacenter Networking AI Assistant.
    <|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    Tell me about datacenter?
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """


Llama3PromptWithFunctions="""<|begin_of_text|>
    <|start_header_id|>system<|end_header_id|>
    you are an expert Datacenter Networking AI Assistant. 
    Given the Following Information: {retrieved_info} respond to user queries.\n{format_instructions}\n
    <|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    {query}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>

"""