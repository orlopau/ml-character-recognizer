import csv


class CSVParser:
    def __init__(self, path: str):
        self.f = open(path, "U")
        self.csv_reader = csv.reader(self.f, delimiter=",")

    def next_line(self):
        line = next(self.csv_reader, None)
        if line is None:
            print("End of file reached!")
            self.f.close()
            return None
        else:
            return self.parse_line(line)

    def parse_line(self, line: []):

        # noinspection PyDictCreation
        data = {'uid': '',
                'char': '',
                'paths': [],
                'minX': float('inf'),
                'maxX': -float('inf'),
                'minY': float('inf'),
                'maxY': -float('inf')}

        data['uid'] = line.pop(0)
        data['char'] = line.pop(0)

        current_path = []

        current_coord_pair = []

        while len(line) > 0:
            char = line.pop(0)
            if char == ",":
                raise Exception('invalid state!')
            elif CSVParser.is_number(char):
                value = float(char)

                current_coord_pair.append(value)

                if len(current_coord_pair) == 1:
                    data['minX'] = min(data['minX'], value)
                    data['maxX'] = max(data['maxX'], value)
                elif len(current_coord_pair) == 2:
                    data['minY'] = min(data['minY'], value)
                    data['maxY'] = max(data['maxY'], value)

                if len(current_coord_pair) == 2:
                    current_path.append((current_coord_pair[0], current_coord_pair[1]))
                    current_coord_pair = []

            elif char == "x":
                data['paths'].append(current_path)
                current_path = []

        return data

    @staticmethod
    def is_number(numbro):
        try:
            float(numbro)
        except ValueError:
            return False
        return True


def calc_center_of_mass(paths):
    sum_x = 0
    sum_y = 0

    len_coords = 0

    for path in paths:
        len_coords += len(path)
        for coord in path:
            sum_x += coord[0]
            sum_y += coord[1]

    return [sum_x / len_coords, sum_y / len_coords]


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

    for path in paths:
        normalized_path = []
        for coords in path:
            normalized_coords = (
                normalize(coords[0] + x_increase / 2, min_x, max_x + x_increase) * scale,
                normalize(coords[1] + y_increase / 2, min_y, max_y + y_increase) * scale
            )
            normalized_path.append(normalized_coords)
        normalized_paths.append(normalized_path)

    return normalized_paths


def normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)
