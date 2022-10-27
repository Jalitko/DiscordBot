FROM ubuntu:20.04

RUN apt-get update -y
RUN apt --fix-broken install

RUN apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libcurl3-gnutls libdrm2 libgbm1 
RUN apt-get install -y libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libwayland-client0 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils

RUN apt-get install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb


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