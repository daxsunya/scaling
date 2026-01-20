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

