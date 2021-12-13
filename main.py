import quantization
from PIL import Image
import spotify_handler

quantizer = quantization.median_cut_quantizer()
quantizer.median_cut(quantizer.load_img('img.jpg'))

for color in quantizer.palette:
        palette_img = Image.new('RGB', (10, 10), (int(color[0]), int(color[1]), int(color[2])))
        palette_img.show()
        palette_img.close()