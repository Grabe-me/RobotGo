FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry install --no-interaction --no-ansi

COPY . /app

RUN poetry run python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. app/robotgo/static/proto_files/test.proto

CMD ["poetry", "run", "python", "main.py"]
