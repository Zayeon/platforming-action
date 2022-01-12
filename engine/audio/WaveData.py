import wave
from openal.al import *


class WaveData:
    def __init__(self, filepath):
        with wave.open(filepath, "rb") as wfile:
            self.nframes = wfile.getnframes()
            self.nchannels = wfile.getnchannels()
            self.sample_rate = wfile.getframerate()
            self.sample_width = wfile.getsampwidth()
            self.size = self.nframes * self.sample_width
            self.data = wfile.readframes(self.nframes)

    def get_format(self):
        if self.nchannels == 1:
            return AL_FORMAT_MONO8 if self.sample_rate == 1 else AL_FORMAT_MONO16
        else:
            return AL_FORMAT_STEREO8 if self.sample_rate == 1 else AL_FORMAT_STEREO16