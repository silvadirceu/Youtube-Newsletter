FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/youtube_manager/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/youtube_manager/requirements.txt

COPY . /code/youtube_manager

CMD ["uvicorn", "youtube_manager.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8001"]
