import csv


class CSVParser:
    def __init__(self, path: str, scale: float):
        self.f = open(path, "U")
        self.scale = scale
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

        data = {
            'char': line.pop(0),
            'paths': []
        }

        current_path = []

        while len(line) > 0:
            char = line.pop(0)
            if char == ",":
                pass
            elif CSVParser.is_number(char):
                current_path.append(float(char) * self.scale)
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
