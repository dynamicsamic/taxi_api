from fastapi import FastAPI

from src.handlers import router as handler_rounter

app = FastAPI()
app.include_router(handler_rounter)
