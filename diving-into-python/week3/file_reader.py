import sys


class FileReader(object):
    """
        Class FileReader helps read data from file
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        try:
            with open(self.file_path, 'r') as rfile:
                return ''.join(rfile.readlines())
        except IOError:
            return ""


if __name__ == '__main__':
    reader = FileReader(sys.argv[1])
    print(reader.read())
