from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers.login import router as loginRouter
from Backend.routers.user import router as userRouter
from Backend.routers.register import router as registerRouter
from Backend.routers.admin import router as adminRouter

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

app.include_router(adminRouter)