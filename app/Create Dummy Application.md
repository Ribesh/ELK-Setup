## Build and Run the Python Application in Docker
```bash
git clone https://github.com/Ribesh/ELK-Setup.git logger-application

cd logger-application/app
```

## Edit the `app.py` 
>Edit `LOGSTASH_HOST` to update the **ELK IP address**
```bash
LOGSTASH_HOST = "<your-logstash-host>"
```

>Build & Run the code
```bash
docker compose up -d --build
```


## Verify if the application is generating logs
```bash
docker logs -f logdemo
```