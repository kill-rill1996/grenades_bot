# grenades_bot

### start app
```
$ sudo docker build -t tg_bot . && sudo docker run -d --name grenades_bot --network grenades-network --ip 172.23.0.22 tg_bot
```

### stop app and delete container
```
$ sudo docker stop grenades_bot && sudo docker rm grenades_bot
```