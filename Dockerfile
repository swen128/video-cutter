FROM python:3.8.0-alpine3.10

RUN apk add --no-cache ffmpeg

# Install the required Python packages.
WORKDIR /workdir
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
