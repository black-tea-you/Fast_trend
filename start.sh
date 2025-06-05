#!/bin/bash
# .env 파일의 모든 변수를 현재 셸로 내보내기
export $(grep -v '^#' .env | xargs)

chmod +x start.sh

# FastAPI 앱 실행 (8000 포트)
uvicorn app.main:app --host 0.0.0.0 --port 8000