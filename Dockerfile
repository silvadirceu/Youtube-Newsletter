FROM python:3.9

WORKDIR /code

COPY ./youtube_manager/requirements.txt /code/youtube_manager/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/youtube_manager/requirements.txt

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY ./youtube_manager /code/youtube_manager

CMD ["uvicorn", "youtube_manager.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]