import os
from fastapi import FastAPI
from dotenv import load_dotenv
from database.db import Base, engine
from routes import user_routes


load_dotenv()

# Create the database tables
Base.metadata.create_all(bind=engine)
app_title = os.getenv("APP_TITLE")
app = FastAPI(title=app_title)
app.include_router(user_routes.router)

app_host=os.getenv("HOSTNAME")
app_port=int(os.getenv("PORT"))

@app.get("/")
async def root():
    return {"message": "Welcome to f`app_title`"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app_host, port=app_port, reload=False)