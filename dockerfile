# 1) 베이스 이미지를 Python + Java가 설치된 형태로 받거나, 직접 설치
FROM python:3.11-slim

# 2) Java (OpenJDK) 설치 (konlpy 용)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless && \
    rm -rf /var/lib/apt/lists/*

# 3) 작업 디렉토리 설정
WORKDIR /app

# 4) requirements.txt 복사 및 의존성 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5) 소스 코드 복사
COPY . /app

# 6) Java Home 설정 (konlpy가 JVM을 찾을 수 있도록)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 7) 기본 PORT를 8000으로 지정 (로컬 디폴트, Render 런타임에서는 덮어쓰기 됨)
ENV PORT=8000

# 8) 컨테이너 기동 명령 (JSON-form + sh -c -> $PORT 치환)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
