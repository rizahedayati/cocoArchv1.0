# syntax=docker/dockerfile:1

FROM python:3.6-slim-buster
FROM docker
COPY --from=docker/buildx-bin:latest /buildx /usr/libexec/docker/cli-plugins/docker-buildx
RUN docker buildx version
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]