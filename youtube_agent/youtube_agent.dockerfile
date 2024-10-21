FROM python:3.11.5

WORKDIR /code

COPY ./youtube_agent/requirements.txt /code/youtube_agent/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/youtube_agent/requirements.txt

COPY ./youtube_agent /code/youtube_agent

RUN pip install --no-cache-dir --upgrade "langflow==1.0.16"

COPY ./youtube_newsletter_package/requirements.txt /code/youtube_newsletter_package/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/youtube_newsletter_package/requirements.txt

COPY ./youtube_newsletter_package /code/youtube_newsletter_package

CMD ["uvicorn", "youtube_agent.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8003"]
