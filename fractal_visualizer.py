import numpy as np
import cmath
from PIL import Image

def generate_sinusoid_fractal(width, height, x_min, x_max, y_min, y_max, max_iter, c):
    fractal_data = np.zeros((height, width), dtype=np.uint16)
    escape_radius = 100.0

    for iy in range(height):
        cy = y_min + (y_max - y_min) * iy / (height - 1)

        for ix in range(width):
            cx = x_min + (x_max - x_min) * ix / (width - 1)
            z = complex(cx, cy)
            n = 0
            while n < max_iter:
                try:
                    z = cmath.sin(z) + c
                except OverflowError:
                    n = max_iter
                    break

                if abs(z) > escape_radius:
                    break

                n += 1

            fractal_data[iy, ix] = n

    return fractal_data

def colorize_fractal(fractal_data, max_iter):
    height, width = fractal_data.shape
    image = Image.new('RGB', (width, height))
    pixels = image.load()

    for iy in range(height):
        for ix in range(width):
            n = fractal_data[iy, ix]

            if n == max_iter:
                color = (0, 0, 0)
            else:
                r = (n * 5) % 255
                g = (n * 3) % 255
                b = (n * 2) % 255
                color = (r, g, b)

            pixels[ix, iy] = color

    return image

image_width = 800
image_height = 600
x_min, x_max = -8.0, 16.0
y_min, y_max = -10.0, 10.0
max_iterations = 1000 # Увеличение этого значения добавляет детали, но замедляет генерацию


c_param = complex(-0.05, 0.05) # Значения можете изменять, чтобы узор менялся

output_filename = "sinusoid_fractal.png"

print(f"Генерация фрактала с c = {c_param}...")
fractal_data = generate_sinusoid_fractal(
    image_width, image_height,
    x_min, x_max, y_min, y_max,
    max_iterations, c_param
)

print("Раскрашивание изображения...")
fractal_image = colorize_fractal(fractal_data, max_iterations)

print(f"Сохранение изображения в {output_filename}")
fractal_image.save(output_filename)

print("Готово!")
