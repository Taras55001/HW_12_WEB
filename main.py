from fastapi import FastAPI


from src.routes import users
from src.routes import contacts
app = FastAPI()

app.include_router(users.router)
app.include_router(contacts.router)


@app.get("/")
def read_root():
    return {"message": "Applicontaction started"}