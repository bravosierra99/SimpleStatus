#theoretically optomized for all things fastapi
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


#all initialization that hopefully will change infrequently
RUN apt-get update && apt-get -yq install npm node.js
RUN python -m pip install aiofiles


#make a directory for the static files and install dependencies
RUN mkdir /SimpleStatusWeb
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
ENV LOGGING_PATH=/tmp/ss.log
ENV STATIC_PATH=/SimpleStatusWeb/build
