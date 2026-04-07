# 파이썬 경량화 이미지를 베이스로 사용합니다.
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# OpenCV 동작에 필요한 시스템 패키지 설치 및 캐시 지우기 (최적화)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 종속성 파일 먼저 복사 (Docker 빌드 캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
