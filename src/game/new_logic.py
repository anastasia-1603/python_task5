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
        self.board[self.curr_y][self.curr_x] = self.curr_block_color
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
        self.board = b[:self.board_height-1]
        self.board.insert(self.board_height - 1, last_row)
        return True

    def take_block(self, x):
        y = self.find_bottom_block(x)
        self.set_color_at(self.curr_x, self.curr_y, self.color_at(x, y))
        self.remove_block(x, y)

    def try_move(self, new_x, new_y):
        if new_x < 0 or new_x > self.board_width - 1:
            return False
        self.curr_x = new_x
        self.curr_y = new_y
        return True

    def set_block(self, x):
        y = self.find_bottom_block(x) + 1
        self.set_color_at(x, y, self.curr_block_color)
        self.set_color_at(self.curr_x, self.curr_y, BlockColors.WHITE)

    def remove_block(self, x, y):
        self.set_color_at(x, y, BlockColors.NO_COLOR)
        self.removed_blocks = self.removed_blocks + 1

    def find_bottom_block(self, column):
        row = 0
        while self.color_at(column, row) != BlockColors.NO_COLOR:
            row = row + 1
        return row - 1

    def find_bottom_block_in_board(self):
        row = 0
        for i in range(self.board_width):
            cur_row = self.find_bottom_block(i)
            if cur_row > row:
                row = cur_row
        return row
