FROM python:3.8

WORKDIR /iatos-app

COPY requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1 ffmpeg

COPY ./src ./src

COPY ./static ./static

COPY ./templates ./templates

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]