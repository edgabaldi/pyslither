class Column:

    def __init__(self, name, length, type=str):
        self.name = name
        self.length = length
        self.type = type

    def parse(self, value):
        if self.type is int:
            try:
                value = int(float(value))
            except ValueError:
                value = 0
            return value
        return value.strip()
