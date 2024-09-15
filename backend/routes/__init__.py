from fastapi import APIRouter,Security,Depends,WebSocket,WebSocketDisconnect,Request,FastAPI,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from routes.Completion import Completion
from routes.ChatCompletion import ChatCompletion
from routes.Embedding import Embedding
from routes.document import FileUploader
from routes.search import FileSearch
from routes.RAG import RAG
from tools.oidc import OpenIDConnect
from conf.constants import CONF
from conf.types import CreateCompletionRequest
from conf.models import ApiQuery,SearchQuery,SearchResponse
import logging

router=APIRouter()
A=Completion()
B=ChatCompletion()
C=RAG()
D=Embedding()
E=FileUploader()
F=FileSearch()

def create_app():
    app=FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
app=create_app()
oidc=OpenIDConnect(scope=CONF.scope,client_id=CONF.client_id,client_secret=CONF.client_secret,sso_host=CONF.sso_host)

@app.get("/login")
@oidc.require_login
async def login(request:Request,code:str):
    logging.info('Login Redirect Received')
    logging.debug({"user_session": request.sess_info})
    path1=f"/Auth?sessionId={request.sess_info['id']}"
    return RedirectResponse(f"{request.url.scheme}://{request.url.netloc}{path1}")

@app.get("/auth")
@oidc.verify_session
async def auth(request:Request,sessionId:str):
    logging.debug('Session Request received with Session ID: %s',sessionId)
    return {'sessionId_state':request.sess_info['state']}

@router.post('/Completion')
@oidc.verify_session
@A._get_ai_response(request=Request,body=CreateCompletionRequest)
def post(request:Request,body:CreateCompletionRequest):
    log.info('Received Completion')
    return {}

@router.post('/ChatCompletion')
@oidc.verify_session
@B._get_ai_response(request=Request,query=ApiQuery)
def post(request:Request,query:ApiQuery):
    log.info('Received Completion')
    return {}

@router.post('/RAG')
@oidc.verify_session
@C._get_ai_response(request=Request,query=ApiQuery)
def post(request:Request,query:ApiQuery):
    log.info('Received Completion')
    return {}

@router.post('/Embedding')
@oidc.verify_session
@D._get_ai_response(request=Request,query=ApiQuery)
def post(request:Request,query:ApiQuery):
    log.info('Received Completion')
    return {}


@router.post("/document")
@oidc.verify_session
@E._upload(request=Request,file=UploadFile)
async def upload_file(request:Request,file: UploadFile):
    return {}

@router.post("/search", response_model=SearchResponse, status_code=200)
@oidc.verify_session
@F._search(request=Request,query=SearchQuery)
def search(request:Request,query:SearchQuery):
    return {}


app.include_router(router)


# _llama2_proxy: Optional[TransformersLLM] = None
# _llama3_proxy: Optional[TransformersLLM] = None
# _codellama_proxy: Optional[TransformersLLM] = None

# llama2_inner_lock=Lock()
# llama2_outer_lock=Lock()
# llama3_inner_lock=Lock()
# llama3_outer_lock=Lock()
# codellama_inner_lock=Lock()
# codellama_outer_lock=Lock()

# def set_llama_proxy():
#     global _llama2_proxy
#     global _llama3_proxy
#     global _codellama_proxy
#     e=LLMLoader()
#     _llama2_proxy=e()
    # _llama2_proxy,_llama3_proxy,_codellama_proxy=e()
    # log.debug(_llama2_proxy)
    # log.debug(_llama3_proxy)
    # log.debug(_codellama_proxy)

# def get_llama2_proxy():
#     llama2_outer_lock.acquire()
#     release_outer_lock = True
#     log.debug('Trying to acquire Lock')
#     try:
#         llama2_inner_lock.acquire()
#         log.debug('Iner Lock Aquired')
#         try:
#             llama2_outer_lock.release()
#             release_outer_lock = False
#             log.debug('Making LLM Available be proceed with request')
#             yield _llama2_proxy
#         finally:
#             llama2_inner_lock.release()
#             log.debug('Inner Lock Released now.')
#             release_outer_lock = False
#     finally:
#         if release_outer_lock:
#             llama_outer_lock.release()
#             log.debug('Outer Lock Released now.')

# def get_llama3_proxy():
#     llama3_outer_lock.acquire()
#     release_outer_lock = True
#     try:
#         llama3_inner_lock.acquire()
#         try:
#             llama3_outer_lock.release()
#             release_outer_lock = False
#             log.debug(_llama3_proxy)
#             yield _llama3_proxy
#         finally:
#             llama3_inner_lock.release()
#     finally:
#         if release_outer_lock:
#             llama3_outer_lock.release()

# def get_codellama_proxy():
#     codellama_outer_lock.acquire()
#     release_outer_lock = True
#     try:
#         codellama_inner_lock.acquire()
#         try:
#             codellama_outer_lock.release()
#             release_outer_lock = False
#             log.debug(_codellama_proxy)
#             yield _codellama_proxy
#         finally:
#             codellama_inner_lock.release()
#     finally:
#         if release_outer_lock:
#             codellama_outer_lock.release()

# @app.on_event("startup")
# async def startup_event():
#     app.state.llama2=get_chatllm2()
    # app.state.llama3=get_chatllm3()
    # app.state.codellama=get_codellm()



# @router.post('/llama2/Completion')
# @A._get_ai_response(request=Request,query=Query,llama_proxy = Depends(get_llama2_proxy))
# def post(request:Request,query:Query,llama_proxy: LLMLoader = Depends(get_llama2_proxy)):
#     log.info('Received LLAMA2 PROXY')
#     return {}


# @router.post('/llama3/Completion')
# @A._get_ai_response(request=Request,query=Query,llama_proxy = Depends(get_llama3_proxy))
# def post(request:Request,query:Query,llama_proxy: LLMLoader = Depends(get_llama3_proxy)):
#     log.info('Received LLAMA3 PROXY')
#     return {}


# @router.post('/codellama/Completion')
# @A._get_ai_response(request=Request,query=Query,llama_proxy = Depends(get_codellama_proxy))
# def post(request:Request,query:Query,llama_proxy: LLMLoader = Depends(get_codellama_proxy)):
#     log.info('Received LLAMA3 PROXY')
#     return {}


# @router.post('/llama2/ChatCompletion')
# # @oidc.verify_login
# @A._get_ai_response(request=Request,query=Query,llama_proxy = Depends(get_llama2_proxy))
# def post(request:Request,query:Query,llama_proxy: LLMLoader = Depends(get_llama2_proxy)):
#     log.info('Received LLAMA2 PROXY')
#     return {}


# @router.post('/llama3/ChatCompletion')
# @A._get_ai_response(request=Request,query=Query,llama_proxy = Depends(get_llama3_proxy))
# def post(request:Request,query:Query,llama_proxy: LLMLoader = Depends(get_llama3_proxy)):
#     log.info('Received LLAMA3 PROXY')
#     return {}


# @router.post('/codellama/ChatCompletion')
# @A._get_ai_response(request=Request,query=Query,llama_proxy = Depends(get_codellama_proxy))
# def post(request:Request,query:Query,llama_proxy: LLMLoader = Depends(get_codellama_proxy)):
#     log.info('Received LLAMA3 PROXY')
#     return {}






    
    

# @app.get("/sessions/mine/")
# @oidc.verify_session
# async def session(request:Request,sessionId:str | None=None):
#     logging.debug('Session Request received with Session ID: %s',sessionId)
#     return {'sessionId_state':request.sess_info['state']}


# @app.websocket("/ws/llama2/ChatCompletion/{room_id}")
# async def websocket_chat(websocket: WebSocket, room_id: str):
#     log.info('Trying websocket connection')
#     await manager.connect(room_id, websocket)
#     log.info('Websocket Connection established')
#     # q=asyncio.Queue()
#     # job_done=object()
#     # ch=QueueCallbackHandler(q,websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             data=json.loads(data)
#             data=Query(**data)
#             log.debug(data)
#             input_prompt=run_validator(data)
#             q=asyncio.Queue()
#             job_done=object()
#             ch=QueueCallbackHandler(q,websocket)
#             async def run(websocket):
#                 log.info('I am run job and i have started')
#                 await asyncio.sleep(0.1)
#                 llama2=next(get_llama2_proxy())
#                 log.debug(llama2)
#                 llama2.callbacks.append(ch)
#                 llmchain:Runnable = input_prompt | llama2
#                 await llmchain.ainvoke([data.userMessage],stream=True,job_done=job_done)
#                 # await app.state.llama2.agenerate([input_prompt.format(query=data.userMessage)],stream=True,job_done=job_done)
#                 llama2.callbacks.remove(ch)
#             asyncio.gather(asyncio.ensure_future(run(websocket)))
#             log.info('Initiated both the jobs')
#     except Exception:
#         log.error("Got an exception ")
#         log.error(traceback.format_exc())
#         # llama2.callbacks.remove(ch)
#         await manager.disconnect(room_id, websocket)




# @app.post('/llm/RAGChatCompletion')
# @B._get_ai_response()
# def post(request:Request,query:Query):
#     return {}


# @app.websocket("/ws/RAGChatCompletion/{room_id}")
# async def websocket_chat(websocket: WebSocket, room_id: str):
#     log.info('Trying websocket connection')
#     await manager.connect(room_id, websocket)
#     log.info('Websocket Connection established')
#     try:
#         while True:
#             data = await websocket.receive_text()
#             log.debug(data)
#             data=json.loads(data)
#             data=Query(**data)
#             input_prompt=run_validator(data)
#             job_done=object()
#             async def run(websocket):
#                 log.info('I am run job and i have started')
#                 await asyncio.sleep(0.1)
#                 ch=QueueCallbackHandler(q,websocket)
#                 app.state.model.callbacks.append(ch)
#                 await app.state.model.agenerate([input_prompt.format(query=data.userMessage)],run_manager=ch,stream=True,job_done=job_done)
#             asyncio.gather(asyncio.ensure_future(run(websocket)))
#             log.info('Initiated both the jobs')
#     except Exception:
#         log.error("Got an exception ")
#         log.error(traceback.format_exc())
#         await manager.disconnect(room_id, websocket)


        # async def fetchandsend(websocket):
        #     log.info('I am fetch and send job and i have started')
        #     await asyncio.sleep(0.1)
        #     while True:
        #         log.info('waiting for queue to be updated.')
        #         try:
        #             token=q.get_nowait()
        #             while True:
        #                 log.info('Received Token in fetch')
        #                 if token !=job_done:
        #                     log.info('sending Token to UI')
        #                     log.info(token)
        #                     try:
        #                         await websocket.send_text(token)
        #                         await asyncio.sleep(0.1)
        #                     except Exception as e:
        #                         log.error(e)
        #                     # await websocket.receive_text()
        #                     token = q.get_nowait()
        #                 else:
        #                     log.info('All tokens sent')
        #                     break
        #             break
        #         except:
        #             log.info('Waiting for tokens')
        #             await asyncio.sleep(0.1)
        #             continue
        #     log.info('I am ending fetch and send')



        # async def run():
        #     ch=QueueCallbackHandler(q)
        #     await asyncio.sleep(0.1)
        #     app.state.model.callbacks=[ch]
        #     app.state.model(input_prompt,stream=True,job_done=job_done)
        
        # async def fetchandsend():
        #     await asyncio.sleep(0.1)
        #     while True:
        #         try:
        #             token=q.get_nowait()
        #             log.info('Received Token')
        #             if token !=job_done:
        #                 log.info('sending Token')
        #                 await websocket.send_text(token)
        #             else:
        #                 log.info('All tokens sent')
        #                 break
        #         except:
        #             log.info('Waiting for tokens')
        #             continue

        # await asyncio.gather(*[asyncio.ensure_future(run()),asyncio.ensure_future(fetchandsend())])
        # log.info('I set the LLM and fetch job to run in future')
        
        
        
        # async def _run():
        #     await asyncio.sleep(0.1)
        #     ch=QueueCallbackHandler(q)
        #     app.state.model.callbacks=[ch]
        #     log.info('I am LLM Model run, and i have started')
        #     app.state.model(input_prompt,stream=True)
        #     q.put_nowait(job_done)
        #     log.info('I am LLM Model run, and i am closing now')
        
        # async def _fetch_and_send(ws):
        #     log.info('I am fetch and send, and i have started')
        #     global q
        #     await asyncio.sleep(1)
        #     next_token=''
        #     # q.put_nowait(next_token)
        #     while not q.empty() or next_token != job_done:
        #         next_token=q.get()
        #         log.info('I see a new token in queue')
        #         if next_token is job_done:
        #             log.info('I got job_done, breaking the loop')
        #             break
        #         else:
        #             log.info('sending it to UI')
        #             await ws.send_text(next_token)
        #             continue
        #             # await websocket.receive()
                
                
        #     log.info('Looping finished, queue is empty')
        
        # await asyncio.gather(_fetch_and_send(websocket),_run())
        
        # log.info('I have started both the jobs in parallel')




            # asyncio.ensure_future(_run())
            # log.info('I have enabled LLM to run in the background')
            # asyncio.ensure_future(_fetch_and_send(websocket))
            # log.info('I am done sending the tokens to UI')
            

            # websocket.send_text(next(app.state.model(input_prompt,stream=True)))





            # async def _run():
            #     await app.state.model(input_prompt,stream=True)
            # done,other=await asyncio.wait([
            #         asyncio.ensure_future(_run()),
            #         asyncio.ensure_future(ch.aiter())
            #     ])
            
            




            # for i in range(10):
            #     await asyncio.sleep(0.01)
            #     await websocket.send_text(f'{i}')
                # await websocket.receive_text()
            # streamer=StreamingLLMCallbackHandler(websocket)
            # app.state.model.callbacks=[streamer]
            # app.state.model(input_prompt,stream=True)
            # for i,chunk in streamer:
            #     await websocket.send_text(chunk)
            # asyncio.ensure_future(app.state.model(input_prompt,stream=True))
            # log.info('Sent Input to LLM, waiting for token generation')
            # async for chunk in streamer.aiter():
            #     log.info(chunk)
            #     await asyncio.sleep(0.1)

          
