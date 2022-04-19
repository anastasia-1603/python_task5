import sys
import logic

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QDesktopWidget, QApplication, QVBoxLayout, QWidget, \
    QHBoxLayout, QPushButton


class AntiTetris(QMainWindow):

    def __init__(self):
        super().__init__()

        self.game_board = GameFrame(self)  # todo start game and game over
        self.setCentralWidget(self.game_board)  # todo  взятие нескольких блоков
        self.status_bar = self.statusBar()
        self.game_board.msg2Statusbar[str].connect(self.status_bar.showMessage)
        self.game_board.start()
        self.setStyleSheet("background-color: white;")
        # todo удаление, если цвета сопадают
        self.resize(800, 600)  # todo логика удаления
        self.setWindowTitle('Тетрис наоборот')  # todo убрать у из curr block
        self.show()


class GameFrame(QFrame):
    msg2Statusbar = pyqtSignal(str)
    SPEED = 30

    def __init__(self, parent):
        super().__init__(parent)
        self.board = logic.Board()
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)
        self.label = QLabel(self)

    def squareWidth(self):
        return self.contentsRect().width() // self.board.board_width

    def squareHeight(self):
        return self.contentsRect().height() // self.board.board_height

    def start(self):
        self.msg2Statusbar.emit(str(self.board.removed_blocks))
        self.timer.start(GameFrame.SPEED, self)

    def game_over(self):
        self.board.clear()
        self.label.setText("Game over")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: blue;"
                                 "background-color: white;"
                                 "font: bold 100px;")
        self.label.move(0, 0)
        self.label.resize(self.contentsRect().width(), self.contentsRect().height())
        button = QPushButton('Restart', self)
        button.resize(100, 50)
        button.move(300, 450)
        button.setStyleSheet("background-color: white;"
                             "color: black;"
                             "font: bold 20px;")
        button.clicked.connect(self.on_restart)
        layout = QVBoxLayout(self.label)
        layout.setAlignment(Qt.AlignBottom)
        layout.addWidget(button)
        self.label.show()
        self.timer.stop()

    @pyqtSlot()
    def on_restart(self):
        self.label.hide()
        self.timer.start(self.SPEED, self)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            logic.move_left(self.board)
            self.update()

        elif key == Qt.Key_Right:
            logic.move_right(self.board)
            self.update()

        elif key == Qt.Key_Return:
            logic.on_enter(self.board)
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
                if color != logic.BlockColors.NO_COLOR:
                    x = rect.left() + (j * self.squareWidth())
                    y = rect.top() + (i * self.squareHeight())
                    curr_x = rect.left() + (self.board.curr_x * self.squareWidth())
                    curr_y = rect.top() + (self.board.curr_y * self.squareHeight())
                    self.draw_block(painter, x, y, color)
                    self.draw_block(painter, curr_x, curr_y, self.board.curr_block_color)
        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.board.move_down() is False:
                self.game_over()
                self.msg2Statusbar.emit("Game over")

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
    app = QApplication(sys.argv)
    tetris = AntiTetris()
    sys.exit(app.exec_())
