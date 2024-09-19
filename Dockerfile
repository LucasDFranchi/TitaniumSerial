FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-pip \
    protobuf-compiler \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/output
WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY proto/titanium.proto /app/titanium.proto
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/nanopb/nanopb.git /app/nanopb

CMD ["/bin/bash", "-c", "protoc --python_out=./ nanopb/generator/proto/nanopb.proto -o ./output/nanopb_pb2.py && \
    protoc -I./nanopb/generator/proto -I. --python_out=. titanium.proto -o ./output/titanium_pb2.py"]
