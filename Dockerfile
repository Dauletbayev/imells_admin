FROM python:3.12

COPY . /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]