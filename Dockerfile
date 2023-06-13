FROM python:3.9.5

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /opt/back

COPY app/ .

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload