from data_util.paths.path_reader import CSVParser
from PIL import Image, ImageDraw
import os
import csv
import numpy as np
import string


def preprocess_paths(paths, max_x, min_x, max_y, min_y, scale, padding):
    width = max_x - min_x
    height = max_y - min_y

    rel_pad_x = width * padding
    rel_pad_y = height * padding

    max_x += rel_pad_x
    min_x -= rel_pad_x

    max_y += rel_pad_y
    min_y -= rel_pad_y

    width = max_x - min_x
    height = max_y - min_y

    x_increase = 0
    y_increase = 0

    # square characters
    if height > width:
        x_increase += height - width
    else:
        y_increase += width - height

    # normalize all values
    normalized_paths = []

    for single_path in paths:
        normalized_path = []
        for coords in single_path:
            normalized_coords = (
                normalize(coords[0] + x_increase / 2, min_x, max_x + x_increase) * scale,
                normalize(coords[1] + y_increase / 2, min_y, max_y + y_increase) * scale
            )
            normalized_path.append(normalized_coords)
        normalized_paths.append(normalized_path)

    return normalized_paths


def normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)


def get_index_of_char(char):
    return string.ascii_uppercase.index(char)


if __name__ == "__main__":
    real_path = "../../../datasets/real"

    parser = CSVParser(os.path.join(real_path, "data.csv"))

    with open(os.path.join(real_path, "dataset.csv"), 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')

        while True:
            data = parser.next_line()
            if data is None:
                break
            else:
                normalized_paths = preprocess_paths(data['paths'], data['maxX'], data['minX'], data['maxY'], data['minY'], scale=128, padding=.15)

                img = Image.new('L', (128, 128), color='black')
                draw = ImageDraw.Draw(img)

                for line in normalized_paths:
                    draw.line(line, fill='white', width=6)

                resized_img = img.resize((28, 28), resample=Image.ANTIALIAS)

                img_array = np.asarray(resized_img).reshape(28*28)

                csv_line = np.append(get_index_of_char(data['char']), img_array)
                writer.writerow(csv_line.tolist())
