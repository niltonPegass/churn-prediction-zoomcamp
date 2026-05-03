FROM python:3.14.4

WORKDIR /app

COPY requirements.txt
RUN pip install -r requirements.txt

COPY ["predict.py", "./"]
COPY ["model/model_C=1.0.bin", "./model/"]

EXPOSE 8080

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:8080", "predict:app"]
