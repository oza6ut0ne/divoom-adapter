import cv2
import numpy as np
import sys

WIDTH = 10
HEIGHT = 10

PALETTE_AURABOX = {
    'black' : 0,
    'red'   : 1,
    'green' : 2,
    'yellow': 3,
    'blue'  : 4,
    'pink'  : 5,
    'aqua'  : 6,
    'white' : 7
}

PALETTE_BGR = {
    'black' : [0, 0, 0],
    'red'   : [0, 0, 255],
    'green' : [0, 255, 0],
    'yellow': [0, 255, 255],
    'blue'  : [255, 0, 0],
    'pink'  : [255, 0, 255],
    'aqua'  : [255, 255, 0],
    'white' : [255, 255, 255]
}


def get_aura_color(pixel):
    min_norm = np.sqrt(255**2 + 255**2 + 255**2)
    nearest_color = 'black'

    for color in PALETTE_BGR.keys():
        bgr = PALETTE_BGR.get(color)
        norm = np.linalg.norm(pixel - bgr)

        if norm < min_norm:
            min_norm = norm
            nearest_color = color

    return PALETTE_AURABOX.get(nearest_color)


def replace_colors(img, from_colors, to_colors):
    if len(from_colors) != len(to_colors):
        print('number of colors must be same')
        return img

    copy = img.copy()
    for from_color, to_color in zip(from_colors, to_colors):
        copy[copy == from_color] = -(to_color + 1)

    copy[copy < 0] = np.abs(copy[copy < 0]) - 1
    return copy


def replace_white_by_black(img):
    from_colors = [PALETTE_AURABOX.get('white')]
    to_colors = [PALETTE_AURABOX.get('black')]
    return replace_colors(img, from_colors, to_colors)


def convert_image_to_aura(img, white_to_black=False):
    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)
    img_int = np.vectorize(int)(img)
    converted_image = np.tile(np.asarray([0]), (HEIGHT, WIDTH, 1))

    for y in range(HEIGHT):
        for x in range(WIDTH):
            converted_image[y, x] = get_aura_color(img_int[y, x])

    if white_to_black:
        converted_image = replace_white_by_black(converted_image)

    return converted_image


def get_image_bytes(img, white_to_black=False):
    if white_to_black:
        img = replace_white_by_black(img)

    image_bytes = []
    it = img[:, :, 0].flat

    for i in it:
        byte = (next(it) << 4) + i
        image_bytes.append(int(byte))

    return image_bytes


if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    converted_image = convert_image_to_aura(img)
    cv2.imwrite('aura.bmp', converted_image)
