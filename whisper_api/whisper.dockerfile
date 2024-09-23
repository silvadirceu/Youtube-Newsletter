FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/whisper_api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/whisper_api/requirements.txt

COPY . /code/whisper_api

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
