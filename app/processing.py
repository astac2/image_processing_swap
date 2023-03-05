import io
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image

num_of_channels = 3


def save_image(func):
    def wrapper(*args, **kwargs):
        image = func(*args, **kwargs)
        if image is not None:
            img_path = os.path.join("static", func.__name__ + "result.png")
            image.save(img_path)
        else:
            img_path = None
        return image, img_path

    return wrapper


def load_image(file_name: str) -> Image:
    try:
        image_box = Image.open(file_name)
        return image_box
    except:
        return None


@save_image
def transform(image: Image, vertical: bool = True) -> Image:
    new_img = Image.new("RGB", (image.width, image.height))
    if vertical:
        half_width = image.width // 2
        # Разбиваем изображение
        left_half = image.crop((0, 0, half_width, image.height))
        right_half = image.crop((half_width, 0, image.width, image.height))
        new_img.paste(right_half, (0, 0))
        new_img.paste(left_half, (half_width, 0))
    else:
        half_height = image.height // 2
        # Разбиваем изображение
        left_half = image.crop((0, 0, image.width, half_height))
        right_half = image.crop((0, half_height, image.width, image.height))
        new_img.paste(right_half, (0, 0))
        new_img.paste(left_half, (0, half_height))

    # Собираем новое изображение
    return new_img


@save_image
def color_distribution(image: Image) -> Image:
    if image is not None:
        image = np.array(image)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        colors = np.zeros((3, 256), dtype=int)  # 3 x 256
        color_for_plot = ["red", "green", "blue"]
        for i in range(num_of_channels):
            unique, counts = np.unique(image[:, :, i], return_counts=True)
            colors[i, unique] = counts
        for i in range(num_of_channels):
            ax.set_axis_off()
            ax.plot(colors[i], color=color_for_plot[i])
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        buffer = io.BytesIO()
        canvas.print_figure(buffer, format="png")
        buffer.seek(0)
        img = Image.open(buffer)
        return img
    else:
        None
