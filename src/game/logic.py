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
    if board.curr_block_color.color == BlockColors.WHITE:
        board.take_block(board.curr_x)
    else:
        board.set_block(board.curr_x)


def random_block():
    return Block(BlockColors(random.randint(2, len(BlockColors) - 1)))


class Block(object):
    def __init__(self, color=BlockColors.NO_COLOR):
        self.color = color

    def set_color(self, color):
        self.color = color


class Board(object):

    def __init__(self, board_width=10, board_height=15, init_rows=3):
        self.board_width = board_width
        self.board_height = board_height
        self.init_rows = init_rows
        self.curr_x = self.board_width - 1
        self.curr_y = self.board_height - 1
        self.curr_block = Block(BlockColors.WHITE)
        self.board = [Block()] * self.board_width * self.board_height
        self.removed_blocks = 0

    def block_at(self, x, y):
        return self.board[(y * self.board_width) + x]

    def set_block_at(self, x, y, block):
        self.board.insert((y * self.board_width) + x, block)

    def change_color(self, x, y, color):
        self.board[(y * self.board_width) + x].set_color(color)

    def fill_board(self, rows):
        for i in range(rows):
            for j in range(self.board_width):
                self.set_block_at(j, i, random_block())

    def fill_with_blocks(self, x1, y1, x2, y2):
        for i in range(y1, y2):
            for j in range(x1, x2):
                self.set_block_at(j, i, random_block())

    def take_block(self, x):
        y = self.find_bottom_block(x)
        self.curr_block.set_color(self.block_at(x, y).color)
        self.remove_block(x, y)

    def try_move(self, new_x, new_y):
        if new_x < 0 or new_x > self.board_width - 1:
            return False
        self.curr_x = new_x
        self.curr_y = new_y
        return True

    def set_block(self, x):
        y = self.find_bottom_block(x) + 1
        self.change_color(x, y, self.curr_block.color)
        self.curr_block.set_color(BlockColors.WHITE)

    def remove_block(self, x, y):
        self.change_color(x, y, BlockColors.NO_COLOR)
        self.removed_blocks = self.removed_blocks + 1

    def find_bottom_block(self, column):
        row = 0
        while self.block_at(column, row).color != BlockColors.NO_COLOR:
            row = row + 1
        return row - 1

    def find_bottom_block_in_board(self):
        row = 0
        for i in range(self.board_width):
            cur_row = self.find_bottom_block(i)
            if cur_row > row:
                row = cur_row
        return row
