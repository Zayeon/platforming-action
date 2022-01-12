from openal.al import *


class Source:

    def __init__(self):
        self.source_id = ctypes.c_uint(0)
        alGenSources(1, ctypes.pointer(self.source_id))

    def delete(self):
        self.stop()
        alDeleteSources(1, self.source_id)

    def play(self, buffer):
        self.stop()
        buffer = ctypes.c_int(buffer.value)
        alSourcei(self.source_id, AL_BUFFER, ctypes.c_int(buffer.value))
        self.resume()

    def pause(self):
        alSourcePause(self.source_id)

    def resume(self):
        alSourcePlay(self.source_id)

    def stop(self):
        alSourceStop(self.source_id)

    def set_volume(self, volume):
        alSourcef(self.source_id, AL_GAIN, volume)

    def set_pitch(self, pitch):
        alSourcef(self.source_id, AL_PITCH, pitch)

    def set_position(self, x, y, z):
        alSource3f(self.source_id, AL_POSITION, x, y, z)

    def set_velocity(self, x, y, z):
        alSource3f(self.source_id, AL_VELOCITY, x, y, z)

    def set_looping(self, loop):
        alSourcei(self.source_id, AL_LOOPING, AL_TRUE if loop else AL_FALSE)

    def is_playing(self):
        playing = ctypes.c_int(0)
        alGetSourcei(self.source_id, AL_SOURCE_STATE, ctypes.POINTER(ctypes.c_int)(playing))
        return playing.value == AL_PLAYING