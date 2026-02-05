# Build and Run the Python Application in Docker
```bash
git clone https://github.com/Ribesh/ELK-Setup.git logger-application
cd logger-application/app

docker compose up -d --build
```


## Verify application generating logs
```bash
docker logs -f logdemo
```