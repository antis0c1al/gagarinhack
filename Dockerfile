FROM python:3.10-slim
WORKDIR /app

COPY . /app

VOLUME /app/data

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install ffmpeg

RUN pip3 install -r requirements.txt

RUN chmod +x /app/baseline.py

CMD ["python3","/app/baselinen.py"]
