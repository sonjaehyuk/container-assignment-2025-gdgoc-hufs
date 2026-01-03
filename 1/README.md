# 과제 1

## 배포판 이미지에서 Python 설치

```dockerfile
FROM fedora:43

WORKDIR /app

RUN dnf -y upgrade && dnf install -y python3 python3-pip && dnf clean all

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
EXPOSE 80

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]
```

> [!TIP]
> python을 설치하고 불필요한 종속성 없애주기

```shell
docker build -t assignment:1.0 -f Dockerfile
```

## Python 이미지 사용

```dockerfile
FROM python:3.14

WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
EXPOSE 80

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]
```

> [!TIP]
> python을 설치할 필요는 없지만 불필요한 종속성을 제거해주기.

```shell
docker build -t assignment:1.1 -f Dockerfile2
```
