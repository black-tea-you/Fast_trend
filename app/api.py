from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from app.db import engine
from app.logic import extract_keywords

router = APIRouter()

class TitleInput(BaseModel):
    titles: list[str]

@router.get("/titles")
def get_titles():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT title FROM news ORDER BY id DESC LIMIT 1000"))
        return {"titles": [row[0] for row in result.fetchall()]}

@router.post("/analyze")
def analyze(input: TitleInput):
    keywords = extract_keywords(input.titles)
    return {"keywords": keywords}
