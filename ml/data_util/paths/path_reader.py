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

        data = dict({'uid': line.pop(0), 'char': line.pop(0), 'paths': [], 'minX': float('inf'), 'maxX': -float('inf'), 'minY': float('inf'), 'maxY': -float('inf')})

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
