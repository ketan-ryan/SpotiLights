from PIL import Image
import numpy as np

# Implementation based on this article https://en.wikipedia.org/wiki/Median_cut
class median_cut_quantizer:
    # Will result in a palette with 2^x colors
    MAX_ITERATIONS = 4
    MAX_WIDTH = 64
    palette = []

    def load_img(self, img_path):
        img = Image.open(img_path)

        # We don't need lots of detail, so we can shrink the image
        if img.size[0] > self.MAX_WIDTH:
            height_percent = self.MAX_WIDTH / float(img.size[1])
            width_size = int((float(img.size[0]) * float(height_percent)))
            img = img.resize((width_size, self.MAX_WIDTH), Image.NEAREST)

        pixels_array = np.asarray(img)
        vals = pixels_array.shape[2]
        rgb_arr = [[]]
        # Flatten 3D array into 1D array
        flattened = pixels_array.flatten()
        # The array now looks like RGB RGB RGB or RGBA RGBA RGBA
        for index in range(0, len(flattened), vals):
            r = flattened[index]
            g = flattened[index + 1]
            b = flattened[index + 2]
            rgb_arr.append([r, g, b])

        rgb_arr.remove([])
        # Convert to numpy array so we can use numpy operations on it
        rgb_arr = np.array(rgb_arr)
        return rgb_arr


    def find_max_range(self, arr):
        max_r, max_g, max_b = np.nanmax(arr, axis=0)
        min_r, min_g, min_b = np.nanmin(arr, axis=0)

        red_range = max_r - min_r
        green_range = max_g - min_g
        blue_range = max_b - min_b

        biggest_range = max(red_range, green_range, blue_range)

        if biggest_range == red_range:
            return 0
        elif biggest_range == green_range:
            return 1
        elif biggest_range == blue_range:
            return 2


    def median_cut(self, array, depth=MAX_ITERATIONS):
        # Base case - average the values in the bucket
        if depth == 0:
            self.palette.append(np.mean(array, axis=0))
            return

        mr = self.find_max_range(array)
        # Sort by column
        array = array[np.argsort(array[:, mr])]
        # Split array down the middle
        middle_index = len(array) // 2

        return self.median_cut(array[:middle_index], depth - 1), self.median_cut(array[middle_index:], depth - 1)


if __name__ == '__main__':
    quantizer = median_cut_quantizer()
    quantizer.median_cut(quantizer.load_img('test2.jpg'))

    for color in quantizer.palette:
        palette_img = Image.new('RGB', (10, 10), (int(color[0]), int(color[1]), int(color[2])))
        palette_img.show()
        palette_img.close()