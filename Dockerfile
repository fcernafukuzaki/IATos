FROM alpine:3.10

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /iatos-web-app

COPY requirements.txt .

#RUN pip --no-cache-dir install -r requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt

#RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1 

COPY ./src ./src

COPY ./static ./static

COPY ./templates ./templates

COPY app.py .

EXPOSE 5000

CMD ["python3", "app.py"]