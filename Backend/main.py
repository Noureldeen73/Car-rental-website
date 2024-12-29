from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.login import router as loginRouter
from routers.user import router as userRouter
from routers.register import router as registerRouter

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loginRouter)
app.include_router(userRouter)
app.include_router(registerRouter)
