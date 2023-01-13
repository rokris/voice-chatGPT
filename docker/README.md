# Speech Recognition Chatbot

This is a chatbot that uses speech recognition and OpenAI's GPT-3 to generate responses.

---
## How it works

1. The chatbot prompts the user for input.
2. It generates a response using the user's input and conversation history.
3. The chatbot prints and speaks the response.

With this chatbot, you can have a conversation with it just like you would with a human!  Give it a try and see what it can do.

---
## Build Docker images
```bash
docker build -t snorkelground_voice_chatgpt .
```

---
## Install PulseAudio
```bash
brew install pulseaudio
nano /usr/local/Cellar/pulseaudio/14.2/etc/pulse/default.pa
    ### Network access (may be configured with paprefs, so leave this commented
    ### here if you plan to use paprefs)
    load-module module-esound-protocol-tcp
    load-module module-native-protocol-tcp
```
---
## Start the PulseAudio on the MAC
```bash
pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1 --daemon -vvvv
pulseaudio --check -v
pactl list short sinks
```

---
## Stop PulseAudio on the MAC
```bash
pulseaudio --kill
```

---
## Run the Docker from MAC
```bash
docker run --rm -it -v ~/.config/pulse:/home/pulseaudio/.config/pulse snorkelground_voice_chatgpt
```

---
## Test from inside Docker
```bash
docker run --rm -it -v ~/.config/pulse:/home/pulseaudio/.config/pulse --entrypoint "/bin/bash" snorkelground_voice_chatgpt
```

---
## Test sound from lokal MAC
```bash
paplay ~/Downloads/test.wav
```

```bash
Test results:
        speaker-test 1.2.8

        Playback device is default
        Stream parameters are 48000Hz, S16_LE, 2 channels
        WAV file(s)
        Rate set to 48000Hz (requested 48000Hz)
        Buffer size range from 96 to 1048576
        Period size range from 32 to 349526
        Using max buffer size 1048576
        Periods = 4
        was set period_size = 262144
        was set buffer_size = 1048576
        0 - Front Left
        1 - Front Right
        Time per period = 3.127385
```
