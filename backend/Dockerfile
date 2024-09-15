FROM python:3.11-slim-bullseye

WORKDIR /app

COPY . .
RUN set -e
RUN apt-get update && \
  apt-get install -y \
  iputils-ping \
  ca-certificates \
  fuse \
  wget \
  unzip \
  git \
  curl
RUN rm -rf /var/lib/apt/lists/*
# Install llama-cpp-python (build with cuda)

RUN python3 -m pip install --upgrade pip

# Install depencencies
RUN  pip install -r requirements.txt

CMD python app.py
