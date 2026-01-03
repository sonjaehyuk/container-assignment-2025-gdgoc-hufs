# 과제 3

## 재현

2에서 한 구성을 통해 컨테이너가 죽어도 가용성이 확보되었음.
그러나 컨테이너가 죽지 않지만 가용성이 없어진 경우 여전히 서비스가 불가능함.

replica가 설정되었다면 replica만큼 아래 요청을 보내면 서비스 불가능을 확인할 수 있음.

```shell
curl -X POST http://127.0.0.1:18888/simulate/router-nuke
```

## livenessProbe

deployment에 livenessProbe를 설정해서 실패 시 재시작하도록 만들 수 있음. 

```yaml
  livenessProbe:
    httpGet:
      path: /healthz
      port: 80
    initialDelaySeconds: 10
    periodSeconds: 5
    timeoutSeconds: 2
    failureThreshold: 3
```

설정 다시 적용

```shell
kubectl apply -f=deployment.yaml
```

다시 접속 및 테스트

```shell
minikube service myservice
```

## HEALTHCHECK

`docker-compose.yaml`의 watcher처럼 컨테이너의 상태를 계속 감시하는 형태로도 해결할 수 있음.
