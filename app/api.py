from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from app.db import engine
from app.logic import extract_keywords
from datetime import date

router = APIRouter()

#날짜 범위 입력력
class DateRangeInput(BaseModel):
    start_date: date  # ex) 2017-01-02
    end_date: date    # ex) 2017-01-30

@router.post("/analyze")
def analyze_by_date_range(input: DateRangeInput):
    #날짜 유효성 검사: end_date가 start_date보다 앞서면 에러
    if input.end_date < input.start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date must be the same or after start_date."
        )

    # 최대 30일 범위 지정정
    delta = (input.end_date - input.start_date).days
    if delta > 30:
        raise HTTPException(
            status_code=400,
            detail="Date range cannot exceed 30 days."
        )

    # DB에서 해당 기간 내 기사 제목 조회
    with engine.connect() as conn:
        sql = text("""
            SELECT title 
            FROM news 
            WHERE DATE(create_time) BETWEEN :start_date AND :end_date
        """)
        result = conn.execute(
            sql,
            {
                "start_date": input.start_date,
                "end_date": input.end_date
            }
        )
        titles = [row[0] for row in result.fetchall()]

    # 결과가 없으면 빈 리스트와 메시지 반환
    if not titles:
        return {
            "keywords": [],
            "message": f"No articles found between {input.start_date} and {input.end_date}."
        }

    # 키워드 분석
    keywords = extract_keywords(titles)
    return {"keywords": keywords}

