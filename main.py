import os
import time
import threading
import quantization
from PIL import Image
import spotify_handler
from datetime import datetime
from datetime import timedelta


quantizer = quantization.MedianCutQuantizer()
sp = spotify_handler.SpotifyHandler()
sleeping_time = 0.1
start_time = datetime.now()
start_time = time.time()


def second_elapsed():
    return (round(time.time(), 5) - round(start_time, 5)).is_integer()

# while True:
#     sp.get_song_info()
#     if second_elapsed():
#         if sp.has_song_changed():
#             print('Song has changed')
#             sp.get_art()
#             quantizer.median_cut(quantizer.load_img('img.jpg'))
#             for color in quantizer.palette:
#                     palette_img = Image.new('RGB', (10, 10), (int(color[0]), int(color[1]), int(color[2])))
#                     palette_img.show()
#                     palette_img.close()
#             os.remove('img.jpg')


while True:
    sp.get_song_info()
    if sp.has_song_changed():
        print('Song has changed')
        sp.get_art()
        quantizer.median_cut(quantizer.load_img('img.jpg'))
        for color in quantizer.palette:
                palette_img = Image.new('RGB', (10, 10), (int(color[0]), int(color[1]), int(color[2])))
                palette_img.show()
                palette_img.close()
        os.remove('img.jpg')

    else:
        timer = threading.Timer(sleeping_time, sp.has_song_changed)
        timer.start()
