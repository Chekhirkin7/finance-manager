from fastapi import FastAPI
from fastapi_app.routes.users import router as users_router
from fastapi_app.routes.transactions import router as transactions_router
from fastapi_app.routes.auth import router as auth_router


app = FastAPI()

app.include_router(users_router)
app.include_router(transactions_router)
app.include_router(auth_router)



@app.get("/")
def read_root():
    return {"message": "Hello"}