from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QInputDialog, QFileDialog
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
        self.name = ''

    def setupUI(self):
        self.setGeometry(500, 100, 1200, 800)
        self.setWindowTitle('Редактор карт')
        self.btns = []
        for i in range(0, 600, 15):
            row = []
            for j in range(0, 900, 15):
                btn = QPushButton(self)
                btn.resize(15, 15)
                btn.move(100 + j, 100 + i)
                btn.clicked.connect(self.colorise)
                btn.setStyleSheet(f"background-color: {self.colors[1].name()}")
                row.append(btn)
            self.btns.append(row)
        self.r_btn = QPushButton(self)
        self.r_btn.move(1000, 400)
        self.r_btn.setText('Клетка стены')
        self.r_btn.resize(180, 40)
        self.b_btn = QPushButton(self)
        self.b_btn.move(1000, 450)
        self.b_btn.setText('Свободная клетка')
        self.b_btn.resize(180, 40)
        self.w_btn = QPushButton(self)
        self.w_btn.move(1000, 500)
        self.w_btn.setText('Дополнительные текстуры')
        self.w_btn.resize(180, 40)
        self.save_btn = QPushButton(self)
        self.save_btn.setText('Сохранить карту')
        self.save_btn.move(1000, 750)
        self.save_btn.resize(180, 40)
        self.save_btn.clicked.connect(self.saves)
        self.open_btn = QPushButton(self)
        self.open_btn.setText('Открыть карту')
        self.open_btn.move(1000, 700)
        self.open_btn.resize(180, 40)
        self.open_btn.clicked.connect(self.open_map)

    def open_map(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать карту', '', "Картинка (*.txt)")[0]
        with open(fname, encoding='utf-8', mode='r') as f:
            level = list(f.readlines())
            level = [list(i.strip('\n')) for i in level]
        self.name = fname.split('/')[-1].rstrip('.txt')
        free, walls, another = self.check()
        for i, row in enumerate(self.btns):
            for j, btn in enumerate(row):
                if level[i][j] == free:
                    btn.setStyleSheet(f"background-color: {self.colors[1].name()}")
                elif level[i][j] == walls:
                    btn.setStyleSheet(f"background-color: {self.colors[0].name()}")
                elif level[i][j] == another:
                    btn.setStyleSheet(f"background-color: {self.colors[2].name()}")
                else:
                    btn.setStyleSheet(f"background-color: {QColor(0, 255, 0).name()}")

    def change_color(self):
        if self.sender().text() == 'Клетка стены':
            self.current_color = 0
        elif self.sender().text() == 'Свободная клетка':
            self.current_color = 1
        elif self.sender().text() == 'Дополнительные текстуры':
            self.current_color = 2

    def colorise(self):
        self.sender().setStyleSheet(f"background-color: {self.colors[self.current_color].name()}")

    def saves(self):
        name = self.run()
        if not name:
            return
        try:
            f = open(f'{name}.txt', encoding='utf-8', mode='w')
        except Exception as ex:
            self.statusBar().showMessage('Неверное имя файла!')
            return
        free, walls, another = self.check()
        for rows in self.btns:
            row = ''
            for btn in rows:
                if btn.styleSheet() == 'background-color: #000000':
                    row += free
                if btn.styleSheet() == 'background-color: #ffffff':
                    row += another
                if btn.styleSheet() == 'background-color: #ff0000':
                    row += walls
            row += '\n'
            f.write(row)
        f.close()

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Введите название",
                                                "Как вы назовёте файл?", text=self.name)
        if ok_pressed:
            return name

    def check(self):
        free, ok_pressed1 = QInputDialog.getInt(
            self, "Введите кодировку пустой клетки", "Кодировка пустой клетки",
            0, 0, 9, 1)
        wall, ok_pressed2 = QInputDialog.getInt(
            self, "Введите кодировку клетки стены", "Кодировка стены",
            2, 0, 9, 1)
        another, ok_pressed3 = QInputDialog.getInt(
            self, "Введите кодировку дополнительной текстуры", "Кодировка дополнительной текстуры",
            1, 0, 9, 1)
        if not ok_pressed1:
            free = '0'
        if not ok_pressed2:
            wall = '5'
        if not ok_pressed3:
            another = '9'
        return str(free), str(wall), str(another)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Level_maker()
    ex.show()
    sys.exit(app.exec())
