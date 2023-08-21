#多个router的入口

from fastapi import FastAPI
from rubatochat.api.v1.apikeys import app as apikeys_router
from rubatochat.api.v1.chat import app as chat_router
from rubatochat.api.v1.auth import app as auth_router


#主路由
app = FastAPI()
app.include_router(apikeys_router, tags=["apikeys"])
app.include_router(chat_router, tags=["chat"])
app.include_router(auth_router, tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=6660)

