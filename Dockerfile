FROM python:3.13-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv pip install --system .

COPY . .

CMD ["uvicorn", "payments.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
