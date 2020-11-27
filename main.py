import sys
from math import cos, pi, sin

from time import sleep

from PIL import Image
from PIL.ImageQt import ImageQt

from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QWidget
from PyQt5.QtWidgets import QPushButton, QColorDialog

SCREEN_SIZE = [700, 700]

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cw-1-pil.ui', self)
        self.initUI()

    def initUI(self):
        self.setGeometry(1920 - SCREEN_SIZE[0] - 20, 50, *SCREEN_SIZE)
        self.setWindowTitle('Диалоговые окна')

        ## Изображение
        self.pic_size = (400, 400)
        fname = QFileDialog.getOpenFileName(self, # parent_widget
            'Выбрать картинку', # window_title
            '', # starting_path
            'Картинка (*.jpg);;Жаба (*jaba*);;Картинка (*.png);;Все файлы (*)' # filters
        )[0] # ноль, потому что возвращается кортеж (путь, фильтр)

        # загружаем картинки через PIL
        self.origin_pic = Image.open(fname)
        self.curr_pic = Image.open(fname)
        # self.degree = 0

        # переходим из PIL в Qt
        self.qt_pic = ImageQt(self.curr_pic)
        self.pixmap = QPixmap.fromImage(self.qt_pic).scaled(*self.pic_size)
        self.img.setPixmap(self.pixmap)

        self.img.resize(*self.pic_size)

        self.left.clicked.connect(self.turn)
        self.right.clicked.connect(self.turn)

        for button in ['r', 'g', 'b', 'all']:
            getattr(self, button).clicked.connect(self.set_channel)

    def set_channel(self):
        self.curr_pic = self.origin_pic.copy()
        # self.curr_pic = self.curr_pic.copy()
        pxls = self.curr_pic.load()
        w, h = self.curr_pic.size
        for x in range(w):
            for y in range(h):
                r, g, b = pxls[x, y]
                if self.sender() is self.r:
                    pxls[x, y] = r, 0, 0
                elif self.sender() is self.g:
                    pxls[x, y] = 0, g, 0
                elif self.sender() is self.b:
                    pxls[x, y] = 0, 0, b
                else:
                    pass

        # self.curr_pic = self.curr_pic.rotate(self.degree, expand=True)
        self.update()

    def turn(self):
        # self.degree += 90 if self.sender() is self.left else -90
        # self.degree = self.degree - self.degree % 36
        # print(self.degree)

        self.curr_pic = self.curr_pic.rotate(90 if self.sender() is self.left else -90, expand=True)
        self.origin_pic = self.origin_pic.rotate(90 if self.sender() is self.left else -90, expand=True)
        self.update()

    def update(self):
        # Отображаем содержимое QPixmap в объекте QLabel
        # переходим из PIL в Qt
        self.qt_pic = ImageQt(self.curr_pic)
        self.pixmap = QPixmap.fromImage(self.qt_pic).scaled(*self.pic_size)
        self.img.setPixmap(self.pixmap)

    def xs(self, x):
        return SCREEN_SIZE[0] // 2 + x

    def ys(self, y):
        return SCREEN_SIZE[1] // 2 - y

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

'''
QColor https://doc.qt.io/qt-5/qcolor.html

Кроме метода setBrush(), у QPainter есть еще метод setPen(), который также принимает в качестве параметра объект QColor. Разница в том, что кисть задает цвет заливки, а ручка — цвет обводки.

Сам процесс рисования очень похож на тот, с каким мы сталкивались при изучении библиотеки Pillow. Например, чтобы нарисовать прямоугольник, применяем метод drawRect(). В качестве параметров ему передаются координаты левого верхнего угла, длина и высота. Как и в Pillow, существуют различные методы для рисования разных графических объектов, например:

drawArc() — для рисования дуги
drawEllipse() — для эллипсов
drawLine() — для линий
drawPolygon() — для многоугольников
drawText() — для текста

QPainter https://doc.qt.io/qt-5/qpainter.html

Поворот картинки в Qt
self.origin_pic = self.origin_pic.transformed(QTransform().rotate(90))
'''