from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Any, List, Optional, Dict, Union
from typing_extensions import TypedDict, NotRequired, Literal
import datetime

JsonType = Union[None, int, str, bool, List[Any], Dict[str, Any]]

class ApiQuery(BaseModel):
    role: str | None
    roleContent: str | None
    userMessage: str
    top_p: float
    top_k: float
    temperature: float
    max_new_tokens: float
    model: str | None
    stream: bool


class ApiResponse(BaseModel):
    response: str = Field('response to the query here')
    response_type: str = Field('type of the response here')


class SearchQuery(BaseModel):
    query: str
    similarity_top_k: Optional[int] = Field(default=1, ge=1, le=5)

class SearchResponse(BaseModel):
    search_result: str 
    source: str

class JsonFile(BaseModel):
    environment: str
    scope: str
    client_id: str
    client_secret:str
    sso_host:str
    local_ollama: bool = False
    local_ollama_url: str
    llm_model_path: str
    llm_quantized_model_path: str
    db_user:str
    db_password: str
    

class User(BaseModel):
    id: str
    title: str
    givenName:str
    familyName:str
    fullName: str
    email: str
    role: str

class Session(BaseModel):
    redirectPath: str
    accessToken: str
    refreshToken: str
    lastRefresh: str
    expiry: str
    ts: datetime.datetime | None = None
    user: User

class ExecutionDetails(BaseModel):
    Group: str
    Name: str
    Params: List
    Execution_Status: str
    FailureReason: str | None = None
    Initiated_At: datetime.datetime= str(datetime.datetime.now())
    Completed_At: datetime.datetime | None = None

class StatisticsRecord(BaseModel):
    UserName: str
    Email: str
    Room: str
    FullCommand: str
    Created_At:int=datetime.datetime.now()
    ExecutionDetails: ExecutionDetails
