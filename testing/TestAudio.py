import time

from engine.audio.AudioHandler import AudioHandler
from engine.audio.Source import Source

audio_handler = AudioHandler()
audio_handler.set_listener_data([0, 0, 0])

buffer = audio_handler.load_sound("res/sounds/bounce.wav")

source = Source()
x = -5
source.set_position(x, 0, 0)

source.set_looping(True)

source.play(buffer)

inp = None
while inp != "q":
    # inp = input()
    # if inp == "p":
    #     if source.is_playing():
    #         source.pause()
    #     else:
    #         source.resume()

    x += 0.1
    print(x)
    source.set_position(x, 0, 1)
    time.sleep(0.1)

audio_handler.clean_up()