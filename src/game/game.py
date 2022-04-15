import sys
import new_logic

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication


class AntiTetris(QMainWindow):

    def __init__(self):
        super().__init__()

        self.game_board = GameFrame(self)  # todo start game and game over
        self.setCentralWidget(self.game_board)  # todo удаление больше 3 блоков и взятие нескольких
        self.status_bar = self.statusBar()
        self.game_board.msg2Statusbar[str].connect(self.status_bar.showMessage)
        self.game_board.start()
        self.setStyleSheet("background-color: white;")  # todo смещение удаленных блоков вверх и
        # todo удаление, если цвета сопадают
        self.resize(800, 600)  # todo логика удаления
        self.setWindowTitle('Тетрис наоборот')  # todo убрать у из curr block
        self.show()


class GameFrame(QFrame):
    msg2Statusbar = pyqtSignal(str)
    SPEED = 30000

    def __init__(self, parent):
        super().__init__(parent)
        self.board = new_logic.Board()
        self.points = 0
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

    def squareWidth(self):
        return self.contentsRect().width() // self.board.board_width

    def squareHeight(self):
        return self.contentsRect().height() // self.board.board_height

    def start(self):
        self.points = 0
        self.msg2Statusbar.emit(str(self.points))
        self.timer.start(GameFrame.SPEED, self)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            new_logic.move_left(self.board)
            self.update()

        elif key == Qt.Key_Right:
            new_logic.move_right(self.board)
            self.update()

        elif key == Qt.Key_Return:
            new_logic.on_enter(self.board)
            self.update()

        else:
            super(GameFrame, self).keyPressEvent(event)

    def paintEvent(self, event):

        painter = QPainter()
        rect = self.contentsRect()
        board_height = self.board.board_height
        board_width = self.board.board_width
        painter.begin(self)

        for i in range(board_height):
            for j in range(board_width):
                color = self.board.color_at(j, i)
                if color != new_logic.BlockColors.NO_COLOR:
                    x = rect.left() + (j * self.squareWidth())
                    y = rect.top() + (i * self.squareHeight())
                    curr_x = rect.left() + (self.board.curr_x * self.squareWidth())
                    curr_y = rect.top() + (self.board.curr_y * self.squareHeight())
                    self.draw_block(painter, x, y, color)
                    self.draw_block(painter, curr_x, curr_y, self.board.curr_block_color)
        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.board.move_down()
            self.update()
        else:
            super(GameFrame, self).timerEvent(event)

    def draw_block(self, painter, x, y, block_color):
        color_table = [0xFFFFFF, 0xFFFFFF, 0xF5000E, 0xFFA129, 0xFFE70A,
                       0x33EAFF, 0x00A819, 0xC54BA4]
        color = QColor(color_table[block_color.value])
        painter.fillRect(x, y, self.squareWidth(), self.squareHeight(), color)
        painter.setPen(Qt.black)
        painter.drawRect(x, y, self.squareWidth(), self.squareHeight())


if __name__ == '__main__':
    # board = new_logic.Board()
    # new_logic.print_board(board)
    # print(5*"\n")
    # board.move_down()
    # new_logic.print_board(board)
    # new_logic.on_enter(board)
    # print(5*"\n")
    # new_logic.print_board(board)

    app = QApplication(sys.argv)
    tetris = AntiTetris()
    sys.exit(app.exec_())