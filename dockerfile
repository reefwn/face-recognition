FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
  cmake \
  gcc \
  g++ \
  make \
  libopenblas-dev \
  libboost-python-dev \
  libboost-system-dev \
  libboost-thread-dev \
  libboost-filesystem-dev \
  libboost-serialization-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "compare-faces/api.py"]
