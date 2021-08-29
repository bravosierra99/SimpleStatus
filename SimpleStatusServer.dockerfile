FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 80
EXPOSE 8000

RUN apt-get update && apt-get -yq install npm


RUN mkdir /SimpleStatusWeb
WORKDIR /

COPY ./simple-status /app
COPY ./simple-status-web /SimpleStatusWeb
WORKDIR /SimpleStatus

RUN ls
#CMD ["uvicorn", "SimpleStatus/SimpleStatusServer:app", "--host", "0.0.0.0", "--port", "8000"]

WORKDIR /SimpleStatusWeb

RUN npm install
ENV PORT=8080
RUN npm build --production
