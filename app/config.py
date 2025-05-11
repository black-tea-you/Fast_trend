from dotenv import load_dotenv
import os

load_dotenv()  # .env 로드

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise RuntimeError("⚠️ DB_URL 환경변수가 설정되지 않았습니다.")