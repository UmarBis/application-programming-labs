import csv


class ImageIterator:
    def __init__(self, path_to_csv: str):
        self.path_to_csv = path_to_csv
        self.image_paths = None
        self.csvreader = None

    def __iter__(self):

        self.image_paths = open(self.path_to_csv)
        self.csvreader = csv.reader(self.image_paths)
        next(self.csvreader)

        return self

    def __next__(self):

        try:
            return self.csvreader.__next__()
        except StopIteration:
            self.image_paths.close()
            raise StopIteration
