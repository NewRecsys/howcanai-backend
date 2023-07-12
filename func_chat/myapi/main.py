from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.chatroom import chatroom_router
from domain.user import user_router

import uvicorn

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chatroom_router.router)
app.include_router(user_router.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000)