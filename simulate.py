from PIL import Image
import numpy as np
import imageio
import json
import matplotlib.pyplot as plt
import matplotlib.colors as color_conv


def compress(input_png_name):
    img = Image.open(input_png_name)
    img_small = img.resize((64, 32), resample=Image.NEAREST)
    img_small_array = np.array(img_small)
    result = img_small
    result_array = np.array(result)
    png_root_name = input_png_name.split(".")[0]
    list_of_hex = []
    color_set = set()
    counter = 0
    for i in np.ndindex(result_array.shape[:2]):
        rgb = result_array[i]
        # TODO handle images missing the alpha channel
        if len(rgb) == 3:
            hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
        else:
            hex_code = "#{:02x}{:02x}{:02x}{:02x}".format(*rgb)
        counter += 1
        list_of_hex.append({"coordinate": counter, "hex": hex_code})
        color_set.add(hex_code)
        prev = hex_code

    with open("outfile.json", "w") as outfile:
        # JSON file can be rendered in browser.
        json.dump(list_of_hex, outfile)
    return list_of_hex


def draw_pixels(color_list):
    plt.axes()
    k = 0
    j = 0
    heightY = 32
    widthX = 64
    circleRadius = 0.8
    pxp = heightY * widthX

    circles = []
    for i in range(1, pxp + 1):
        circle = None
        k += 1
        if i % (widthX) == 0:
            j += 1
            k = 0
            continue

        color_obj = color_list[i - 1]["hex"]
        # There's a negative on one axis to ensure correct image orientation.
        circle = plt.Circle(
            (72 + (k * circleRadius * 2), -(100 + (j * circleRadius * 2))),
            radius=0.75,
            facecolor=color_conv.to_rgba(color_obj),
            edgecolor=color_conv.to_rgba(color_obj),
            # fill=False,
        )
        plt.gca().add_patch(circle)
    plt.axis("scaled")
    plt.axes().patch.set_facecolor("xkcd:salmon")
    plt.axes().patch.set_facecolor((1.0, 0.47, 0.42))
    plt.show()


if __name__ == "__main__":
    color_list = compress("clock.webp")
    draw_pixels(color_list)
