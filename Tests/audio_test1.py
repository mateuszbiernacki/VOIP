# From https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python Yevhen Kuzmovych

import pyaudio
import wave

"""That record sound from microphone for 5 second and save this to wave file."""

"""Installation of PyAudio is required.
    Windows Example:
        pip install pipwin
        pipwin install pyaudio
    MacOS Example:
        brew install portaudio
        python3 -m pip install pyaudio
    Linux Example (not checked yet):
        sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
        sudo apt-get install ffmpeg libav-tools
        sudo -s
        pip install pyaudio"""

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
