## Python
```bash
python -m venv test

source test/bin/activate
```

## Docker
```bash
docker build -t python-trading-signal .

docker run -d --env-file .env -p 8000:8000 python-trading-signal
```

## Deployment
### Koyeb
```bash
## logs
koyeb service logs respectable-flea/python-trading-signal
```

## Test