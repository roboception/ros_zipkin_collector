FROM ros:melodic-ros-base

RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    netcat-openbsd \
    python-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ros_zipkin_collector.py ./ros_zipkin_collector.py

ENV PYTHONUNBUFFERED 1
STOPSIGNAL SIGINT
CMD [ "python", "ros_zipkin_collector.py" ]
