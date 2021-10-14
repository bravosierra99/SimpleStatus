# SimpleStatus
A dockerized app to receive and display status... simply

## Getting Started
- `docker pull bravosierra99/simple-status`
- `docker run -dp 80:80 bravosierra99/simple-status`
- [Client Code](https://github.com/bravosierra99/SimpleStatusClient) 
  - Instructions for usage are on the repo
- http://**server-ip** in browser

### Logging
Logs are stored in /SimpleStatusWeb/SimpleStatus.log inside the container.  

run the following command to enable debugging for logs
`docker run -e DEBUG=1 -dp 80:80 bravosierra99/simple-status`


## API Documentation
This project uses fastapi, and keeps the default documentation.  Therefore you can access the REST API at http:/**server-ip**/api/docs or http:/**server-ip**/api/redoc
