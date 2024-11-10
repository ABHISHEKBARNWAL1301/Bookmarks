from fastapi import FastAPI 
from connection import  engine
from models import Base
from search.routes import CrudRoute
from auth.routes import AuthRoute


app = FastAPI(
    title="Bookmark API",
    description="API to save and tag articles",
    version="0.1"
)

app.include_router(CrudRoute)
app.include_router(AuthRoute)


# Create all tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)






