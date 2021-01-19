from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtGui import QColor
import sys


class Level_maker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_color = 0
        self.colors = [QColor(255, 0, 0), QColor(0, 0, 0), QColor(255, 255, 255)]
        self.setupUI()
        self.r_btn.clicked.connect(self.change_color)
        self.b_btn.clicked.connect(self.change_color)
        self.w_btn.clicked.connect(self.change_color)

    def setupUI(self):
        self.setGeometry(500, 100, 900, 950)
        self.btns = []
        for i in range(0, 600, 15):
            for j in range(0, 900, 15):
                btn = QPushButton(self)
                btn.resize(15, 15)
                btn.move(100 + i, j)
                btn.clicked.connect(self.colorise)
                btn.setStyleSheet(f"background-color: {self.colors[1].name()}")
                self.btns.append(btn)
        self.r_btn = QPushButton(self)
        self.r_btn.move(750, 400)
        self.r_btn.setText('RED')
        self.b_btn = QPushButton(self)
        self.b_btn.move(750, 450)
        self.b_btn.setText('BLACK')
        self.w_btn = QPushButton(self)
        self.w_btn.move(750, 500)
        self.w_btn.setText('WHITE')
        self.save_btn = QPushButton(self)
        self.save_btn.setText('Сохранить карту')
        self.save_btn.move(750, 800)
        self.save_btn.clicked.connect(self.saves)

    def change_color(self):
        if self.sender().text() == 'RED':
            self.current_color = 0
        elif self.sender().text() == 'BLACK':
            self.current_color = 1
        elif self.sender().text() == 'WHITE':
            self.current_color = 2

    def colorise(self):
        self.sender().setStyleSheet(f"background-color: {self.colors[self.current_color].name()}")
        print(self.sender().styleSheet())

    def saves(self):
        f = open('second_lvl.txt', encoding='utf-8', mode='w')
        row = ''
        for i in range(len(self.btns)):
            if self.btns[i].styleSheet() == 'background-color: #000000':
                row += '0'
            if self.btns[i].styleSheet() == 'background-color: #ffffff':
                row += '9'
            if self.btns[i].styleSheet() == 'background-color: #ff0000':
                row += '5'
            if (i + 1) % 60 == 0:
                row += '\n'
                f.write(row)
                row = ''
        f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Level_maker()
    ex.show()
    sys.exit(app.exec())
