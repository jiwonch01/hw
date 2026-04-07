# 1. 'slim'이 아닌 일반 python:3.12 사용 (이미 필요한 도구들이 많이 들어있음)
FROM python:3.12

# 2. 에러가 계속 나는 apt-get install 과정을 아예 삭제했습니다.
# 일반 python 이미지에는 필요한 기본 라이브러리가 포함되어 있어 바로 설치가 가능할 수 있습니다.

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 전체 코드 복사
COPY . .

# 6. 실행 설정
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]