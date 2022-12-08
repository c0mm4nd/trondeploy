FROM ubuntu:22.04

COPY . /tron
RUN apt update && apt install -y openjdk-8-jre python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /tron

EXPOSE 8090
EXPOSE 50545
EXPOSE 18888
EXPOSE 18888/udp
CMD ["bash", "start.sh"]
