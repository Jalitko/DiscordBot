FROM ubuntu:20.04

# We want the "add-apt-repository" command
RUN apt-get update && apt-get install -y software-properties-common

# Install "ffmpeg"
RUN apt-get update && apt-get install -y ffmpeg

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ ./bot

ENTRYPOINT [ "python3" ]

CMD ["./bot/main.py"]