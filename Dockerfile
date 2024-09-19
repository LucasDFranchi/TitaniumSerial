FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-pip \
    protobuf-compiler \
    dos2unix \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/output
WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY proto/titanium.proto /app/titanium.proto
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/nanopb/nanopb.git /app/nanopb

CMD ["/bin/bash", "-c", "protoc --python_out=/app/output/ nanopb/generator/proto/nanopb.proto && \
    mv /app/output/nanopb/generator/proto/nanopb_pb2.py /app/output/nanopb_pb2.py  && \
    rm -rf /app/output/nanopb && \
    protoc -I./nanopb/generator/proto -I. --python_out=/app/output/ titanium.proto"]
