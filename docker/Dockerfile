FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN apt-get update
RUN apt-get install -y \
alsa-utils \
pulseaudio \
espeak \
build-essential \
libasound2-plugins \
portaudio19-dev \
--no-install-recommends

RUN pip install -r requirements.txt
RUN rm -rf /var/lib/apt/lists/*
RUN /bin/sh -c 'useradd --create-home --home-dir $HOME pulseaudio && usermod -aG audio,pulse,pulse-access pulseaudio && chown -R pulseaudio:pulseaudio $HOME'

WORKDIR /home/pulseaudio
USER pulseaudio
ENV HOME=/home/pulseaudio
ENV PULSE_SERVER=docker.for.mac.localhost

ENTRYPOINT ["python"]
CMD ["/app/snorkelground_voice_chatgpt.py"]
