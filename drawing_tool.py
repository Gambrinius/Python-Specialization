class Canvas(object):
    """
    Base class, which realize simple drawing tool.
    """

    @staticmethod
    def build_board(width, height):
        """
        Method create a new canvas board,
        two-dimensional matrix of width and height size.
        :param width:
        :param height:
        :return: board:
        """
        board = []
        for row_index in range(height + 2):
            if row_index == 0 or row_index == height + 1:
                board.append(['-' for _ in range(width + 2)])
                continue

            line = []
            for column_index in range(width + 2):
                if column_index == 0 or column_index == width + 1:
                    line.append('|')
                else:
                    line.append(' ')
            board.append(line)
        return board

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = self.build_board(width, height)

    def draw_line(self, x1, y1, x2, y2):
        """
        Method create a new line from (x1,y1) to (x2,y2) on canvas board.
        Currently only horizontal or vertical lines are supported.
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        if x2 - x1 > 0:   # draw horizontal line
            for column_index in range(x1, x2 + 1):
                self.board[y1][column_index] = 'x'

        if y2 - y1 > 0:   # draw vertical line
            for row_index in range(y1, y2 + 1):
                self.board[row_index][x1] = 'x'

    def draw_rectangle(self, x1, y1, x2, y2):
        """
        Method create a new rectangle, whose upper left corner is (x1,y1)
        and lower right corner is (x2,y2), on canvas board.
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        # draw horizontal sides of rectangle
        for row_index in (y1, y2):
            for column_index in range(x1, x2 + 1):
                self.board[row_index][column_index] = 'x'

        # draw vertical sides of rectangle
        for row_index in range(y1, y2 + 1):
            self.board[row_index][x1] = 'x'
            self.board[row_index][x2] = 'x'

    def bucket_fill(self, x, y, new_cell, old_cell=None):
        """
        Method fill the entire area connected to (x,y) with chosen "colour" on canvas board.
        The behavior of this is the same as that of the "bucket fill" tool in paint programs.
        :param x:
        :param y:
        :param new_cell:
        :param old_cell:
        :return:
        """

        if old_cell is None:
            old_cell = self.board[y][x]

        if self.board[y][x] != old_cell:
            return

        # change to new colour
        self.board[y][x] = new_cell

        if x > 0:  # left
            self.bucket_fill(x - 1, y, new_cell, old_cell)

        if y > 0:  # up
            self.bucket_fill(x, y - 1, new_cell, old_cell)

        if x < self.width:  # right
            self.bucket_fill(x + 1, y, new_cell, old_cell)

        if y < self.height:  # down
            self.bucket_fill(x, y + 1, new_cell, old_cell)

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.board])


class CanvasError(Exception):
    pass


def main():
    canvas = None
    with open('input1.txt', 'r') as input_file:
        commands = input_file.readlines()

    if not commands[0].startswith('C'):
        raise CanvasError("You can only start drawing if a canvas has been created firstly!")

    with open('output.txt', 'w') as output_file:
        for command in commands:
            if command.startswith('C'):  # create canvas
                args = list(map(lambda i: int(i), command.replace('C ', '').split()))
                canvas = Canvas(*args)
                output_file.write(str(canvas) + '\n')
            elif command.startswith('L'):   # draw line
                args = list(map(lambda i: int(i), command.replace('L ', '').split()))
                canvas.draw_line(*args)
                output_file.write(str(canvas) + '\n')
            elif command.startswith('R'):   # draw rectangle
                args = list(map(lambda i: int(i), command.replace('R ', '').split()))
                canvas.draw_rectangle(*args)
                output_file.write(str(canvas) + '\n')
            elif command.startswith('B'):   # bucket fill
                args = command.replace('B ', '').split()
                colour = args.pop()
                x, y = list(map(lambda i: int(i), args))
                canvas.bucket_fill(x, y, colour)
                output_file.write(str(canvas) + '\n')


if __name__ == '__main__':
    main()
