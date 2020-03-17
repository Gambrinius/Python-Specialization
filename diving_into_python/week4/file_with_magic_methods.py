import tempfile
import os


class File:
    def __init__(self, full_path):
        self.full_path = full_path
        self.iter_file = None

        if not os.path.exists(self.full_path):
            with open(full_path, 'a'):
                pass

    def write(self, content):
        with open(self.full_path, 'w') as f:
            return f.write(content)

    def get_file_name(self):
        return str(os.path.basename(self.full_path).split('.')[0])

    def __add__(self, other):
        with open(self.full_path, 'r') as self_file:
            with open(other.full_path, 'r') as other_file:
                result_string = self_file.read() + other_file.read()

        full_path = os.path.join(
            tempfile.gettempdir(),
            self.get_file_name() + '_' + other.get_file_name() + '.txt'  # new_file_name
        )
        new_file = File(full_path)
        new_file.write(result_string)

        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_file is None:
            self.iter_file = open(self.full_path, 'r')
        return self.iter_file.__next__()

    def __str__(self):
        return self.full_path


if __name__ == '__main__':
    first_file = File('/home/gambrinius/PycharmProjects/Python-Specialization/'
                      'diving-into-python/week4/file1.txt')
    second_file = File('/home/gambrinius/PycharmProjects/Python-Specialization/'
                       'diving-into-python/week4/file2.txt')
    result_file = first_file + second_file

    print(result_file, end='')
    print("new file iteration:")
    for line in result_file:
        print(line, end='')
