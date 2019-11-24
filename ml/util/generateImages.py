from __future__ import absolute_import, division, print_function, unicode_literals
from util.parseCSV import *
from PIL import Image, ImageDraw
import os

parser = CSVParser("data0.csv")

while True:
    data = parser.next_line()
    if data is None:
        break
    else:
        print(data)
        path = os.path.join("imgs", data['char'])
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        normalized_paths = preprocess_paths(data['paths'], data['maxX'], data['minX'], data['maxY'], data['minY'], scale=28)

        img = Image.new('1', (28, 28), color='white')
        draw = ImageDraw.Draw(img)

        for line in normalized_paths:
            draw.line(line)

        img.save(os.path.join(path, str(len(os.listdir(path)))) + ".png")
