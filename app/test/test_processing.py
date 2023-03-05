import os
import random

import numpy as np
import PIL.Image as Image

from app.processing import transform


def test_transform():
    image = Image.new("RGB", (10, 10))
    if not os.path.exists("static"):
        os.mkdir("static")
    for i in range(10):
        for j in range(10):
            image.putpixel(
                (i, j),
                (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
            )
    image_proc, img_path = transform(image, vertical=True)
    assert image_proc is not None
    assert image_proc.size != (0, 0)
    assert os.path.exists(img_path)
    assert np.array_equal(
        np.array(image.crop((0, 0, 5, 10))),
        np.array(image_proc.crop((5, 0, 10, 10))),
    )
    assert np.array_equal(
        np.array(image.crop((5, 0, 10, 10))),
        np.array(image_proc.crop((0, 0, 5, 10))),
    )
