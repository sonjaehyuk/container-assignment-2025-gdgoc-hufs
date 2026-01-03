# 과제 4

```ini
[Unit]
Description=My Assignment
After=network.target

[Service]
Type=simple
ExecStart=docker run --name myassignment --memory 512m --memory-swap 512m assignment:1.1
ExecStop=docker stop myassignment
ExecStopPost=docker rm myassignment
Restart=always # systemd가 스스로 재시작 해줌

[Install]
WantedBy=multi-user.target
```

1. `assignment.service`를 `/etc/systemd/system`으로 옮김.
2. `systemctl daemon-reload`
3. `systemctl start assignment`
4. `docker ps` 및 `systemctl status assignment`로 확인.
5. [과제 2번](../2/README.md)에서 나온 메모리 초과 실험.
6. `systemctl stop assignment`로 컨테이너가 지워지는 것을 확인.
