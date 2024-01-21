FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install --no-interaction --no-ansi

COPY . /app

CMD ["poetry", "run", "python", "main.py"]
