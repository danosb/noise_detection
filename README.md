# noise_detection
A Python script that uses a Raspberry Pi computer to monitor for loud noises. If detected, it sends recording and details of the noise via email.

## Summary

My dog sometimes barks when I'm not home. I wanted to be able to monitor when it happens and be able to react to stop the barking. V1 of this program just listens for loud noises, records, and sends details to my phone via email. 

I'd like to expand the functionality out more to enable responses to sounds, which can be selected. These could include a recording of me telling my dog to be quiet verbally, or a high pitched sound that's audible only to dogs and meant to deter barking. Eventually would be nice to also have in-app notifications rather than using email. That would enable real-time actions, potentially even two-way communication.

I used a Raspberry Pi 3 model B+ and a Playstation Eye connected via USB for recording. The PS Eye was a cheap and simple way to get audio-in working, but proved to be not so simple in terms of audio out. In Linux the default ALSA sound software stuff doesn't play nice with the PS Eye due to it have too many channels. I've read some people had success by using Pulse Audio instead, but for now I'm using analog for audio out.

The biggest hurdle came when trying to install the `pyloudnorm` Python library, which I'm using for analyzing loudness. `pyloudnorm` has a dependency on the `scipy` library, and my Raspberry Pi kept crashing after an hour or two of trying to build the wheel during install. Even compiling and installing `scipy` from source didn't get around the problem. Ended up having to temporarily increase the Pi's swap space to be the same size as the RAM, which allowed `pyloudnorm`/`scipy` to install successfully.

## Setup
1. Get Rasperry Pi and install RaspianOS
2. Ensure audio input is working (nice guide here: https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone)
3. Download noise_detection.py and copy it to local folder
4. Modify credentials for email sending
5. Install required libraries
6. Run with Python

## Hardware
1. Raspberry Pi 3
2. PlayStation Eye (PS3 Eye)

## Software
1. Raspbian GNU/Linux 8 - OS, with Python
2. `pyaudio`, `wave`, `soundfile` Python libraries - for recording and saving audio
3. `datetime` Python library for including date/time in filename/email
4. `pydub` Python library for audio playback
5. `pyloudnorm` Python library for loudness analysis
6. `smtplib`, `email` Python libraries for email sending
7. `os` Python library for file deletion
