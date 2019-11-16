from __future__ import absolute_import, division, print_function, unicode_literals
from util.parseCSV import CSVParser
from PIL import Image, ImageDraw
import os

img = Image.new("1", (40, 40), color="white")

draw = ImageDraw.Draw(img)

draw.line([(0, 0), (40, 40)], fill="black", width=1)

img.save("test.png")

parser = CSVParser("data0.csv", scale=40)

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

        img = Image.new('1', (40, 40), color='white')
        draw = ImageDraw.Draw(img)

        for line in data['paths']:
            draw.line(line)

        img.save(os.path.join(path, str(len(os.listdir(path)))) + ".png")
