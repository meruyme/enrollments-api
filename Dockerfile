FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV TZ="America/Recife"
ENV PYTHONPATH="/code"

WORKDIR /code
RUN python3 -m venv /code/venv

COPY ./requirements.txt /code/
RUN pip3 install -r requirements.txt

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
