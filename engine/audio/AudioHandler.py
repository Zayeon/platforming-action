from openal.al import *
from openal.alc import *

from engine.audio.WaveData import WaveData


class AudioHandler:
    def __init__(self):
        # TODO: Handle all audio output, not just default
        device = alcOpenDevice(None)  # gets default output device
        self.context = alcCreateContext(device, None)
        alcMakeContextCurrent(self.context)

        # Store all buffers locally so we can
        self.buffers = []

    def load_sound(self, file):
        buffer = ctypes.c_uint(0)
        alGenBuffers(1, ctypes.POINTER(ctypes.c_uint)(buffer))
        self.buffers.append(buffer)
        wave_file = WaveData(file)

        alBufferData(buffer, wave_file.get_format(), wave_file.data, wave_file.size, wave_file.sample_rate)

        return buffer

    def set_listener_data(self, position):
        alListener3f(AL_POSITION, position[0], position[1], position[2])
        alListener3f(AL_VELOCITY, 0, 0, 0)

    def clean_up(self):
        for buffer in self.buffers:
            alDeleteBuffers(1, buffer)

        alcDestroyContext(self.context)