import random
import sys
from enum import Enum

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication


class AntiTetris(QMainWindow):

    def __init__(self):
        super().__init__()

        self.game_board = Board(self)  # todo start game and game over
        self.setCentralWidget(self.game_board)  # todo logic.py and game.py
        self.status_bar = self.statusBar()
        self.game_board.msg2Statusbar[str].connect(self.status_bar.showMessage)
        self.game_board.start()
        self.setStyleSheet("background-color: white;")  # todo смещение удаленных блоков вверх
        self.resize(800, 600)  # todo логика удаления
        self.setWindowTitle('Тетрис наоборот')  # todo убрать у из curr block
        self.show()


class BlockColors(Enum):
    NO_COLOR = 0
    WHITE = 1
    RED = 2
    ORANGE = 3
    YELLOW = 4
    BLUE = 5
    GREEN = 6
    PURPLE = 7


def random_block():
    return Block(BlockColors(random.randint(2, len(BlockColors) - 1)))


def fill_list_with_blocks(x1, y1, x2, y2):
    l = []
    for i in range(y1, y2):
        for j in range(x1, x2):
            l.insert(i * Board.BOARD_WIDTH + j, random_block())
    return l


class Block(object):
    def __init__(self, color=BlockColors.NO_COLOR):
        self.color = color

    def set_color(self, color):
        self.color = color


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    BOARD_WIDTH = 10
    BOARD_HEIGHT = 15
    INIT_ROWS = 3
    SPEED = 3000

    def __init__(self, parent):
        super().__init__(parent)
        self.curr_x = self.BOARD_WIDTH - 1
        self.curr_y = self.BOARD_HEIGHT - 1
        self.timer = QBasicTimer()
        self.board = [Block()] * self.BOARD_WIDTH * self.BOARD_HEIGHT
        self.fill_board(self.INIT_ROWS)
        self.removed_blocks = 0
        self.curr_block = Block(BlockColors.WHITE)
        self.setFocusPolicy(Qt.StrongFocus)

    def block_at(self, x, y):
        return self.board[(y * self.BOARD_WIDTH) + x]

    def set_block_at(self, x, y, block):
        self.board.insert((y * self.BOARD_WIDTH) + x, block)

    def change_color(self, x, y, color):
        self.block_at(x, y).set_color(color)

    def squareWidth(self):
        return self.contentsRect().width() // self.BOARD_WIDTH

    def squareHeight(self):
        return self.contentsRect().height() // self.BOARD_HEIGHT

    def fill_board(self, rows):
        for i in range(rows):
            for j in range(self.BOARD_WIDTH):
                self.set_block_at(j, i, random_block())

    def fill_with_blocks(self, x1, y1, x2, y2):
        for i in range(y1, y2):
            for j in range(x1, x2):
                self.set_block_at(j, i, random_block())

    def start(self):
        self.removed_blocks = 0
        self.msg2Statusbar.emit(str(self.removed_blocks))
        self.timer.start(Board.SPEED, self)

    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Left:
            self.try_move(self.curr_x - 1, self.curr_y)

        elif key == Qt.Key_Right:
            self.try_move(self.curr_x + 1, self.curr_y)

        elif key == Qt.Key_Return:
            if self.curr_block.color == BlockColors.WHITE:
                self.take_block(self.curr_x)
            else:
                self.set_block(self.curr_x)
        else:
            super(Board, self).keyPressEvent(event)

    def paintEvent(self, event):

        painter = QPainter()
        rect = self.contentsRect()
        painter.begin(self)

        for i in range(Board.BOARD_HEIGHT):
            for j in range(Board.BOARD_WIDTH):
                block = self.block_at(j, i)
                if block.color != BlockColors.NO_COLOR:
                    x = rect.left() + (j * self.squareWidth())
                    y = rect.top() + (i * self.squareHeight())
                    curr_x = rect.left() + (self.curr_x * self.squareWidth())
                    curr_y = rect.top() + (self.curr_y * self.squareHeight())
                    self.draw_block(painter, x, y, block.color)
                    self.draw_block(painter, curr_x, curr_y, self.curr_block.color)
        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_down()
        else:
            super(Board, self).timerEvent(event)

    def move_down(self):
        bottom_row = self.find_bottom_block_in_board()
        if bottom_row + 1 >= self.BOARD_HEIGHT:
            return False

        board_copy = self.board.copy()
        new_row = [random_block() for _ in range(self.BOARD_WIDTH)]
        self.board = new_row + board_copy
        self.update()
        return True

    def take_block(self, x):
        y = self.find_bottom_block(x)
        self.curr_block.set_color(self.block_at(x, y).color)
        self.remove_block(x, y)
        self.update()

    def try_move(self, new_x, new_y):
        if new_x < 0 or new_x > self.BOARD_WIDTH - 1:
            return False
        self.curr_x = new_x
        self.curr_y = new_y
        self.update()
        return True

    def set_block(self, x):
        y = self.find_bottom_block(x) + 1
        self.change_color(x, y, self.curr_block.color)
        self.curr_block.set_color(BlockColors.WHITE)
        self.update()

    def remove_block(self, x, y):
        self.change_color(x, y, BlockColors.NO_COLOR)
        self.removed_blocks = self.removed_blocks + 1
        self.update()

    def find_bottom_block(self, column):
        row = 0
        while self.block_at(column, row).color != BlockColors.NO_COLOR:
            row = row + 1
        return row - 1

    def find_bottom_block_in_board(self):
        row = 0
        for i in range(Board.BOARD_WIDTH):
            cur_row = self.find_bottom_block(i)
            if cur_row > row:
                row = cur_row
        return row

    def draw_block(self, painter, x, y, block_color):
        color_table = [0xFFFFFF, 0xFFFFFF, 0xF5000E, 0xFFA129, 0xFFE70A,
                       0x33EAFF, 0x00A819, 0xC54BA4]
        color = QColor(color_table[block_color.value])
        painter.fillRect(x, y, self.squareWidth(), self.squareHeight(), color)
        painter.setPen(Qt.black)
        painter.drawRect(x, y, self.squareWidth(), self.squareHeight())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tetris = AntiTetris()
    sys.exit(app.exec_())
