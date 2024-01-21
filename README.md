# Асинхронный gRPC сервис для взаимодействия с роботом в лабиринте.

## Введение

#### В данном проекте был разработан микросервис, реализующий управление роботом в лабиринте с использованием протокола gRPC и асинхронного программирования на Python с помощью asyncio. Роботу необходимо было перемещаться по лабиринту, избегая диагональных перемещений, и рационально достигать заданных целевых точек.

## О сервисе

- Для выборя ближайщей цели и обеспечения нахождения роботом оптимального пути до неё был использован алгоритм [A-star](https://github.com/Grabe-me/RobotGo/tree/master/robotgo/algorythm) (A*)
- Алгоритм интегрирован с gRPC [сервисом](https://github.com/Grabe-me/RobotGo/blob/master/robotgo/api_servers/server.py) с использованием asyncio для обеспечения неблокирующей обработки запросов.

## Запуск из репозитория

- клонирование репозитория


  ```
  git clone https://github.com/Grabe-me/RobotGo

  cd RobotGo
  ```

- установка зависимостей

    
  ```
  pip instal poetry
  poetry install
  ```

- запуск сервера


  ```
  poetry run python main.py
  ```

- сервер по-умолчанию принимает подключения на порт `50051`
## Запуск с Docker

### - amd64

    
  ```
  docker run -p 50051:50051 grabe85me/robot_go_amd64:vol_1
  ```

### - arm

    
  ```
  docker run -p 50051:50051 grabe85me/robot_go_arm:vol_1
  ```

## Подключение

- Пример реализации [клиента](https://github.com/Grabe-me/RobotGo/blob/master/robotgo/api_servers/client.py) для взаимодействия с роботом
- Proto [файл](https://github.com/Grabe-me/RobotGo/blob/master/robotgo/static/proto_files/test.proto) для реализации клиента и создания запросов

#
