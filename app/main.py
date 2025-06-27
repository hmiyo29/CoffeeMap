
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.routes import cafes, reviews
import app.models as models
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        # Try a basic SQL query
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Connected to database"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

app.include_router(cafes.router)
app.include_router(reviews.router)


# Mount templates
templates = Jinja2Templates(directory="app/frontend/templates")

@app.get("/map", response_class=HTMLResponse)
async def get_map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})
