# Raspsound
play wechat voice via raspberry pi

## install dependencies

    sudo apt-get install redis-server nginx
    sudo pip install requests tornado rq rq-dashboard redis

## config nginx (optional)

config nginx with `proxy_pass` to `http://localhost:5000`

```
location ^~ /wx {
  proxy_pass http://localhost:5000;
}
```

## run

    redis-server &
    rq-dashboard &
    rq worker &
    python main.py &
