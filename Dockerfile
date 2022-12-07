FROM python:latest

COPY . /tron
RUN apt update && apt install -y openjdk-8-jre && rm -rf /var/lib/apt/lists/*
WORKDIR /tron

EXPOSE ["50545", "50555", "18888", "18888/udp"]
CMD ["bash", "start.sh"]
