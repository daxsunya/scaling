## Оглавление

- [Масштабирование приложений](#масштабирование-приложений)
  - [Docker registry for Linux Part 1](#docker-registry-for-linux-part-1)
  - [Docker registry for Linux Part 2 & 3](#docker-registry-for-linux-part-2--3)
  - [Docker Orchestration Hands-on Lab](#docker-orchestration-hands-on-lab)
  - [Swarm stack introduction](#swarm-stack-introduction)
  - [Счетчик (docker)](#счетчик-docker)
    - [Промежуточные выводы](#промежуточные-выводы)
    - [Увеличение инстансов БД](#увеличение-инстансов-бд)
      - [Особенности при работе реплицированного сервиса с БД](#особенности-при-работе-реплицированного-сервиса-с-бд)
  - [Счетчик (kubernetes)](#счетчик-kubernetes)

# Масштабирование приложений
## Docker registry for Linux Part 1
<img width="740" height="109" alt="Снимок экрана 2026-01-19 в 21 57 19" src="https://github.com/user-attachments/assets/44d37ac3-f8c6-48e4-a795-b63f93cc91bb" />

<img width="608" height="140" alt="Снимок экрана 2026-01-19 в 21 53 10" src="https://github.com/user-attachments/assets/d16bb3de-34dc-4541-8272-c9c003a65d69" />

<img width="608" height="106" alt="Снимок экрана 2026-01-19 в 21 55 09" src="https://github.com/user-attachments/assets/b0b7decc-cd8d-4a91-b27c-e6a38ff24087" />

## Docker registry for Linux Part 2 & 3
Демонстрация неуспеха/успеха при аутентификации соответственно

<img width="740" height="326" alt="Снимок экрана 2026-01-20 в 22 17 21" src="https://github.com/user-attachments/assets/27b7ac6e-8dd7-45f1-b62e-8c9ef125df6b" />

## Docker Orchestration Hands-on Lab
После перевода ноды в состояние Active назначенных на нее задач нет, так как ранее принадлежащие ей были переназначены на другие ноды (node1 и node3)

Это можно заметить запустив команду `docker ps` на каждой из нод

<img width="740" height="706" alt="Снимок экрана 2026-01-20 в 23 07 41" src="https://github.com/user-attachments/assets/7128db06-ce16-41f3-8337-d3fd1c88035e" />

Для того, чтобы на node2 была назначена задача можно, например, увеличить число реплик приложения:

`docker service update --replicas 7 sleep-app`

После проверим, что новая задача действительно назначена на node2

<img width="740" height="706" alt="Снимок экрана 2026-01-20 в 23 09 16" src="https://github.com/user-attachments/assets/d8248b87-7955-47ee-b0e0-14cb7c579771" />

## Swarm stack introduction
Количество нодов регулируется swarm-ом путем подключения соответствующих нод. Уже после Stack разворачивается на всех доступных нодах. Проверка жизнеспособности поддерживается с помощью описания healthcheck в конфигурационном yaml-файле.

Пример из репозитория задания:

<img width="479" height="286" alt="Снимок экрана 2026-01-20 в 23 32 11" src="https://github.com/user-attachments/assets/f2bd4a2c-5d2c-4bb0-b30f-dbbba3d9ef45" />

## Счетчик (docker)
Проведем сравнение в одинаково выделенных ресурсах, а именно установим в docker-compose для каждого варианта приложения:

- для redis: cpu - 0.5, memory - 512M
- для app: cpu - 0.3, memory - 256M

<img width="597" height="442" alt="Снимок экрана 2026-01-22 в 22 01 52" src="https://github.com/user-attachments/assets/ece16aae-e4fa-46cb-8471-f12295535af7" />

В итоге rps для приложения с одним контейнером выглядит так:

<img width="2928" height="1800" alt="total_requests_per_second_1769107227 751" src="https://github.com/user-attachments/assets/23e652ea-1cab-46d3-9627-845993325bd5" />

- _[подробный отчет](https://github.com/daxsunya/scaling/tree/main/counter-1-container)_

С несколькими:

<img width="2928" height="1800" alt="total_requests_per_second_1769107630 82" src="https://github.com/user-attachments/assets/271b4d37-a5aa-49d4-bc31-1f59d26e3cf5" />

- _[подробный отчет](https://github.com/daxsunya/scaling/tree/main/counter-4-container)_

### Промежуточные выводы
_**Rps для данной конфигурации лучше в варианте с несколькими инстансами**_

_**Redis стал узким местом**_

  При нескольких контейнерах приложения:

  - возрастает количество конкурентных запросов к Redis

  - усиливается контенция за CPU и сетевые ресурсы

  - Redis обрабатывает команды последовательно

  - Redis не успевает обслуживать увеличившееся число клиентов

### Увеличение инстансов БД
Поставим свойство replicas: 1 -> replicas:2 для redis

<img width="2928" height="1800" alt="total_requests_per_second_1769111025 628" src="https://github.com/user-attachments/assets/ffcb4f0c-4765-45b6-87fa-afd7d9b849af" />

- rps немного поднялся но незначительно

- наблюдается более стабильное поведение (временные скачки меньше, чем были раннее)

#### Особенности при работе реплицированного сервиса с БД
Тонкости в работе с реплицированным сервисом с БД заключаются в сохранении данных, их необходимо синхронизировать, иначе может получиться следующее:

<img width="566" height="146" alt="Снимок экрана 2026-01-22 в 22 51 15" src="https://github.com/user-attachments/assets/259daf85-4340-4273-9803-4844d5bee656" />

Получается, что при вызове сервиса попадаем то на один инстанс то на второй и обращаемся к хранилищу каждого, а так как данные не синхронизированы между собой, то ответ непредсказуемый

## Счетчик (kubernetes)
[Файлы конфигурации для запуска](https://github.com/daxsunya/scaling/tree/main/counter-with-kubernetes)

### Запуск
Собрать докер

```
docker build -t counter:latest .
```

Запустить миникуб

```
minikube delete
minikube start --driver=docker
```

Применить файлы конфигурации для миникуб

```
kubectl apply -f redis-deployment.yaml 
kubectl apply -f redis-service.yaml      
kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml
```

Убедиться, что приложение запущено и работает корректно
1. Проверить поды

```
kubectl get po
```
<img width="471" height="100" alt="Снимок экрана 2026-01-23 в 00 05 55" src="https://github.com/user-attachments/assets/bc230838-e39c-4653-ac77-245dc54a4ea6" />
