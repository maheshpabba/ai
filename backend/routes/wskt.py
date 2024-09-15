from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler,BaseCallbackHandler
from typing import Any, AsyncIterator, Dict, List, Literal, Union, cast
from langchain_core.outputs import LLMResult
import asyncio


import logging

log = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[str,WebSocket]= {}
        log.info("Creating a list to hold active connections",self.active_connections)

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if not self.active_connections.get(room_id):
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        log.info("New Active connections are ",self.active_connections)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        log.info("After disconnect active connections are: ",self.active_connections)

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)
        # log.info("Sent a personal msg to , ",websocket)
        # log.info("message", message)

    async def broadcast(self, message: str, room_id: str, websocket: WebSocket):
        for connection in self.active_connections[room_id]:
            if connection != websocket:
                await connection.send_text(message)
                log.info("In broadcast: sent msg to ",connection)




class QueueCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q,websocket):
        self.q = q
        self.q.empty()
        self.websocket=websocket
        

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        # log.info('Received Token, putting in queue')
        # self.q.put_nowait(token)
        await self.websocket.send_text(token)
        await asyncio.sleep(0.01)
        

    def on_llm_end(self, *args, **kwargs: Any) -> None:
        return self.q.empty()
    

manager=ConnectionManager()




