# 과제 2

## 재현

1. 실행
```shell
docker run -d -it -p 18888:80 --rm --memory 512m --memory-swap 512m --name myassignment assignment:1.1
```

2. 확인
```shell
curl http://127.0.0.1:18888/healthz
```

3. 파괴
```shell
curl -d '{"mb":"600","hold_ms":"10000"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:18888/simulate/memory-spike
```

4. 확인
```shell
curl http://127.0.0.1:18888/healthz
```

## Kubernetes

먼저 minikube 내에서 이미지를 찾을 수 있도록 `/1`로 이동해서 빌드.

```shell
minikube image build -t assignment:1.1 -f Dockerfile2 .
```

Deployment 객체와 Service 객체를 가동.

```shell
kubectl apply -f=deployment.yaml -f=service.yaml
```

> [!IMPORTANT]
> **apply**이므로 파일과 실제 kubernetes가 참조 관계에 있는 것이 아님.
> 일회성으로 적용되는 것이기에 업데이트가 있으면 다시 apply해야 하고, 반대로 kubectl 명령으로 (파일과 무관하게) 객체를 삭제하거나 수정할 수 있음.

```shell
minikube service myservice
```

위 명령으로 얻은 URL로 재시작 동작을 검증.
