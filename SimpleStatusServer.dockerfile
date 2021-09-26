#theoretically optomized for all things fastapi
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


#all initialization that hopefully will change infrequently
RUN apt-get update && apt-get -yq install npm node.js
RUN python -m pip install aiofiles


#make a directory for the static files and install dependencies
RUN mkdir /SimpleStatusWeb

##we need local copies of swagger and redoc js/css files
RUN mkdir /SimpleStatusWeb/swagger
WORKDIR /SimpleStatusWeb/swagger
RUN wget https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js
RUN wget https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css
RUN wget https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js

COPY ./simple-status-web/package*.json /SimpleStatusWeb/
WORKDIR /SimpleStatusWeb
RUN npm install

#ok now copy over the static files
COPY ./simple-status /app
COPY ./simple-status-web/ /SimpleStatusWeb
RUN npm run build 


#settings that theoretically should not change
EXPOSE 80
ENV PORT=80
ENV STATIC_PATH=/SimpleStatusWeb/build
ENV SWAGGER_STATIC_PATH=/SimpleStatusWeb/swagger
ENV DEBUG=true
ENV LOGGING_CONFIG_INI="logging.config.ini"
