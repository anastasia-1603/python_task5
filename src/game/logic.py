from enum import Enum
import random


class BlockColors(Enum):
    NO_COLOR = 0
    WHITE = 1
    RED = 2
    ORANGE = 3
    YELLOW = 4
    BLUE = 5
    GREEN = 6
    PURPLE = 7


def move_left(board):
    board.try_move(board.curr_x - 1, board.curr_y)


def move_right(board):
    board.try_move(board.curr_x + 1, board.curr_y)


def on_enter(board):
    if board.curr_block_color == BlockColors.WHITE:
        board.take_block(board.curr_x)
    else:
        board.set_block(board.curr_x)


def print_board(board):
    for y in board.board:
        print(y)


def random_color():
    return BlockColors(random.randint(2, len(BlockColors) - 1))


class Board(object):

    def __init__(self, board_width=10, board_height=15, init_rows=3):
        self.board_width = board_width
        self.board_height = board_height
        self.curr_x = self.board_width - 1
        self.curr_y = self.board_height - 1
        self.curr_block_color = BlockColors.WHITE
        self.board = [[BlockColors.NO_COLOR for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.fill_board(init_rows)
        # self.board[self.curr_y][self.curr_x] = self.curr_block_color
        self.is_visited = [[False for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.removed_blocks = 0

    def color_at(self, x, y):
        return self.board[y][x]

    def set_color_at(self, x, y, color):
        self.board[y][x] = color

    def fill_board(self, rows):
        for i in range(rows):
            self.board[i] = [random_color() for _ in range(self.board_width)]

    def move_down(self):
        bottom_row = self.find_bottom_block_in_board()
        if bottom_row + 2 >= self.board_height:
            return False

        board_copy = self.board.copy()
        last_row = self.board[self.board_height - 1]
        new_row = [[random_color() for _ in range(self.board_width)]]
        b = new_row + board_copy
        self.board = b[:self.board_height - 1]
        self.board.insert(self.board_height - 1, last_row)
        return True

    def move_up(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.color_at(x, y) == BlockColors.NO_COLOR:
                    self.move_up_column(x, y)

    def move_up_column(self, x, y):
        for y in range(y, self.board_height-1):
            self.board[y][x] = self.board[y+1][x]

    def take_block(self, x):
        y = self.find_bottom_block(x)
        self.curr_block_color = self.color_at(x, y)
        self.remove_block(x, y)

    def try_move(self, new_x, new_y):
        if new_x < 0 or new_x > self.board_width - 1:
            return False
        self.curr_x = new_x
        self.curr_y = new_y
        return True

    def set_block(self, x):
        y = self.find_bottom_block(x) + 1
        color = self.curr_block_color
        self.set_color_at(x, y, color)
        if self.count_equal(x, y, color) > 3:
            self.remove_blocks(x, y, color)
            self.move_up()
        self.curr_block_color = BlockColors.WHITE
        self.is_visited = [[False for _ in range(self.board_width)] for _ in range(self.board_height)]

    def remove_blocks(self, x, y, color):
        if x < 0 or x > self.board_width - 1 or y < 0 or y > self.board_height:
            return
        elif self.color_at(x, y) == color:
            self.remove_block(x, y)
            self.remove_blocks(x + 1, y, color)
            self.remove_blocks(x - 1, y, color)
            self.remove_blocks(x, y - 1, color)
            self.remove_blocks(x, y + 1, color)
            self.removed_blocks = self.removed_blocks + 1

    def remove_block(self, x, y):
        self.set_color_at(x, y, BlockColors.NO_COLOR)

    def clear(self):
        self.board = [[BlockColors.NO_COLOR for _ in range(self.board_width)]
                      for _ in range(self.board_height)]

    def count_equal(self, x, y, color):
        count = 0
        if x < 0 or x > self.board_width - 1 or y < 0 or y > self.board_height:
            return 0
        elif self.color_at(x, y) == color and self.is_visited[y][x] is False:
            self.is_visited[y][x] = True
            count = count + 1
            count = count + self.count_equal(x + 1, y, color)
            count = count + self.count_equal(x, y - 1, color)
            count = count + self.count_equal(x - 1, y, color)
            count = count + self.count_equal(x, y + 1, color)
            return count
        else:
            return 0

    def is_have_equal_around(self, x, y, color):
        return ((x-1 > 0 and self.color_at(x-1, y) == color) or
                (x+1 < self.board_width and self.color_at(x+1, y) == color) or
                (y-1 > 0 and self.color_at(x, y-1) == color) or
                (y + 1 < self.board_height and self.color_at(x, y+1) == color))

    def find_bottom_block(self, column):
        row = self.board_height - 2
        while self.color_at(column, row) == BlockColors.NO_COLOR and row >= 0:
            row = row - 1
        return row

    def find_bottom_block_in_board(self):
        row = 0
        for i in range(self.board_width):
            cur_row = self.find_bottom_block(i)
            if cur_row > row:
                row = cur_row
        return row
