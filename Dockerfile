# 1. 베이스 이미지 설정 (가벼운 버전으로 변경)
FROM python:3.12-slim

# 2. 필수 라이브러리 설치 (에러 방지를 위해 설정 추가)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 전체 코드 복사
COPY . .

# 6. 실행 설정 (8000 포트 사용)
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]