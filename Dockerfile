FROM python:3.9-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
