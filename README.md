# 도전 과제

> [!NOTE]
> 예시 답안을 [`/1`](./1/README.md), [`/2`](./2/README.md), [`/3`](./3/README.md), [`/4`](./4/README.md) 디렉토리에서 확인할 수 있습니다.

명령어를 암기하는 방식을 넘어, 실제 마주할 수 있는 여러 딜레마를 체험하고 이에 대한 각자의 견해를 생각/정리해 볼 수 있는 기회를 마련해 드리기 위해 준비하였습니다.

* 본 도전 과제에서는 FastAPI라는 Python 웹 프레임워크를 사용합니다. 
* 소스코드는 여기서 확인할 수 있습니다: https://github.com/sonjaehyuk/container-assignment-2025-gdgoc-hufs 
* 모든 도전 과제는 소스코드 수정 없이 수행할 수 있습니다.
* Python 라이브러리 패키지를 제외하고 외부 의존성(데이터베이스 등)은 없습니다.
* 도전 과제에 나와있는 명령은 명확한 이해를 위해 권한 정보를 가정하지 않았습니다. 실제 사용 시 명령어 앞에 sudo를 붙어야 할 수 있습니다.
* **각 과제는 여러 정답이 존재합니다. 여러분이 고른 방법이 여러분의 정답입니다!**

## 1. 여러 방식으로 이미지 만들어 보기

FastAPI를 실행하기 위해서는 Python이 필요합니다. 이때 이미지의 Base 이미지로 Python(https://hub.docker.com/_/python)을 선택하는 것이 보통입니다.

```dockerfile
FROM python:3.13
```

### 과제/목표

이 소스코드로 2개의 이미지를 만드시오.
* Base 이미지가 [https://hub.docker.com/_/python](https://hub.docker.com/_/python)인 이미지
* Base 이미지가 본인이 가장 선호하는 리눅스 배포판인 이미지

둘 중 하나를 골라 이미지를 빌드하시오.

```shell
docker build -t assignment1:latest . 
```

### 도움말

Python 라이브러리 패키지를 설치하는 명령어입니다(package.json 같은 느낌).
```shell
pip install -r requirements.txt
```

FastAPI 애플리케이션을 실행시키기 위해 사용하는 명령어입니다. 이 명령어가 작동하기 위해서는 80번 포트가 노출되어 있어야 합니다.
```shell
python -m uvicorn main:app --host 0.0.0.0 --port 80 --workers 1
```

## 2. 죽은 컨테이너 살리기

docker는 각 컨테이너마다 호스트의 컴퓨팅 자원 사용을 제한할 수 있는 기능을 포함하고 있습니다.
예를 들어:

|                  |                                 |
|------------------|---------------------------------|
| --memory 용량      | 해당 컨테이너가 사용할 수 있는 최대 메모리 용량입니다. |
| --memory-swap 용량 | 해당 컨테이너가 사용할 수 있는 최대 스왑 용량입니다.  |

스왑은 메모리가 부족할 때 디스크를 메모리처럼 사용하는 기술로, 만약 스왑까지 모두 소진하게 되면 리눅스는 커널을 살리기 위해 사용자 프로세스를 하나씩 종료시킵니다.

--memory-swap로 설정하는 용량은 --memory의 값을 포함하고 있습니다. 예를 들어 --memory-swap 512m --memory 512m으로 설정되면 스왑 공간은 0입니다.

만약 docker에서 자원 용량 값이 명시적으로 주어지지 않으면 컨테이너는 호스트의 모든 자원을 사용할 수 있습니다. 호스트의 상태를 항상 안정되게 유지하고 싶다면 컨테이너에 걸리는 최대 부하를 조절함으로써 호스트를 보호할 수 있습니다.

여기서 문제가 발생합니다.
컨테이너에 이러한 자원 제한을 걸고 실행을 하다가 해당 제한을 넘게 되면 어떻게 될까요? 당연히 컨테이너가 통째로 멈춥니다. 여기서 빠르게 컨테이너를 복구하는 것이 호스트를 지키면서 서비스 가용성도 잘 유지할 수 있는 관건입니다.

### Prelude

주어진 명령어를 따라 컨테이너를 실행하세요.

```shell
docker run -d -it -p 8888:80 --memory 512m --memory-swap 512m --name myassignment localhost/assignment1:latest
```
_--rm 옵션은 본인 선택입니다._

컨테이너 실행 이후 메모리 사용 API 요청을 보내고 컨테이너가 죽는 것을 확인합니다. 동일한 요청을 보낼 수 있으면 curl을 사용하지 않아도 괜찮습니다.

```shell
curl -d '{"mb":"600","hold_ms":"10000"}' -H "Content-Type: application/json" -X POST http://localhost:8888/simulate/memory-spike
```

curl 명령이 오류를 반환하는 것을 확인하고 docker에서 정말 컨테이너가 (어떻게) 죽었는지 확인해 봅시다.

```shell
docker ps;
docker logs myassignment;
```

### 과제/목표
**지금처럼 컨테이너가 갑자기 죽을 때 가능한 한 빠르게 복구할 방법을 마련하시오. 이후, 위 curl 명령을 사용하여 컨테이너가 정상적으로 재시작되는지 검증하시오.**

## 3. 컨테이너는 살아있습니다만?

2번 과제에서는 컨테이너의 상태가 곧 서비스의 상태였습니다. 그러나 컨테이너는 살아있으면서, 서비스로서 가동하기에 불능인 상태가 존재할 수 있습니다. 3번 과제는 이를 탐지하고 복구하는 과제입니다.

### Prelude

주어진 명령어를 따라 컨테이너를 실행하세요.

```shell
docker run -d -it -p 8888:80 --name myassignment localhost/assignment1:latest
```
_--rm 옵션은 본인 선택입니다._

curl 명령어로 상태 확인 API를 호출해 봅시다.
```shell
curl http://localhost:8888/healthz
```

이제 FastAPI 서비스를 살아있으나, 가동 불능인 상태로 만드는 API를 호출해 봅시다.
```shell
curl -X POST http://localhost:8888/simulate/router-nuke
```

다시 상태 확인 API를 호출하여 서비스가 망가졌는지 확인합니다.

### 과제/목표
**컨테이너는 작동하나 서비스가 작동하지 않는 상황을 탐지하고, 이를 가능한 한 빠르게 복구하는 방법을 마련하시오. 이후, 위 curl 명령을 사용하여 서비스 복구가 실제로 이루어지는지 검증하시오.**

### 도움말
Dockerfile에서 HEALTHCHECK 명령어를 사용할 수 있습니다.

```dockerfile
HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD wget -qO- http://localhost:80/healthz || exit 1
```

10초마다 상태 확인을 하면서, 상태 확인 명령어가 실패하거나 3초 타임아웃이 3번 연속 발생하면, 컨테이너 상태가 나쁨으로 전환됩니다. 이를 이용해서 컨테이너 내 서비스 오류를 탐지할 수 있습니다.

## 4. 인프라에서의 타협
리눅스의 모든 프로세스는 1번 프로세스의 자식입니다. 그리고 프로세스는 자식 프로세스를 완전히 제어/감독할 수 있습니다. 이 원칙들을 이용해 1번 프로세스가 전체 시스템 관리를 총괄하도록 만드는 풍조가 생겨났습니다. 그 결과물이 [systemd](https://github.com/systemd/systemd)입니다.

여러분이 Docker를 배우는 동안 여러분의 동료는 systemd를 이용한 시스템 관리를 배웠습니다. 여러분의 동료는 Docker로 배포하는 것은 허용하되, systemd 명령어로 Docker를 관리하기를 원한다는 입장입니다.

여러분은 Docker 컨테이너이면서 동시에 systemd 명령어를 쓸 수 있도록 환경 구성을 해야 합니다.

### 과제/목표
도전 과제 2에서 설정한 메모리 제한이 적용되어야 합니다.
컨테이너가 중지된 경우(메모리 초과) 스스로 재시작할 수 있어야 하며, 이후 systemd 명령어도 사용 가능해야 합니다.
컨테이너 중지 방법은 도전 과제 2에서 제시한 curl 명령과 동일하다고 가정합니다.
아래 systemd 명령어를 지원해야 합니다.

|                                         |                                |
|-----------------------------------------|--------------------------------|
| `systemctl start myassignment.service`  | myassignment 컨테이너를 시작합니다       |
| `systemctl stop myassignment.service`   | myassignment 컨테이너를 중지하고 삭제합니다. |

### 도움말
`/etc/systemd/system/myassignment.service` 파일을 만들면 됩니다.

```ini
[Unit]
Description=My Assignment
After=network.target

[Service]
Type=simple
ExecStart=   여기를 채우세요.
ExecStop=    여기를 채우세요.
ExecStopPost=여기를 채우세요.

[Install]
WantedBy=multi-user.target
```

위는 최소한의 구성으로, **재시작 정책에 따라 달라질 수 있습니다.**

service 파일을 작성했다면 다음 명령어로 service 파일을 적용합니다.

```shell
systemctl daemon-reload
```


현재 service 상태를 확인하고 싶다면 다음 명령어를 사용합니다.

```shell
systemctl status myassignment.service
```

## 5. 논술형

컨테이너는 환경 변화에서도 애플리케이션이 일정하게 동작하도록 지켜주는 기술일까요, 아니면 예상치 못 한 애플리케이션이 시스템 전체에 영향을 주지 않도록 막아주는 안전장치일까요? 여러분은 어느 쪽에 더 가깝다고 보시나요?
