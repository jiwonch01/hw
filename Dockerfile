# 1. 베이스 이미지를 조금 더 넉넉한 버전으로 변경
FROM python:3.12

# 2. 환경 변수 설정 (설치 중 묻는 말에 답하지 않음)
ENV DEBIAN_FRONTEND=noninteractive

# 3. 시스템 패키지 설치 (에러 방지를 위해 하나씩 설치 및 업데이트 강화)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. 작업 디렉토리 설정
WORKDIR /app

# 5. 필요한 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. 전체 코드 복사
COPY . .

# 7. 실행
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]