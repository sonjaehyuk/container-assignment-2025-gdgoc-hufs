FROM fedora:43

WORKDIR /app

RUN dnf -y upgrade && dnf install -y python3 python3-pip && dnf clean all

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
EXPOSE 80

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]
