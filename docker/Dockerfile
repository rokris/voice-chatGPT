FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip && \
apt-get update && \
apt-get install -y \
alsa-utils=1.2.4-1 \
pulseaudio=14.2-2 \
espeak=1.48.15+dfsg-2 \
build-essential=12.9 \
libasound2-plugins=1.2.2-2 \
portaudio19-dev=19.6.0-1.1 \
--no-install-recommends && \
pip install --no-cache-dir -r requirements.txt && \
rm -rf /var/lib/apt/lists/* && \
/bin/sh -c 'useradd --create-home --home-dir $HOME pulseaudio && \
usermod -aG audio,pulse,pulse-access pulseaudio && \
chown -R pulseaudio:pulseaudio $HOME && chmod +x /app/start_voice_chatgpt.sh'

WORKDIR /home/pulseaudio
USER pulseaudio
ENV HOME=/home/pulseaudio
ENV PULSE_SERVER=docker.for.mac.localhost

ENTRYPOINT ["/app/start_voice_chatgpt.sh"]
