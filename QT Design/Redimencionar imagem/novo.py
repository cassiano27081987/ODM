import sys
from design import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap

class Novo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnEscolherarquivo.clicked.connect(self.abrir_imagem)
    
    def abrir_imagem(self):
        imagem, _ = QFileDialog.getOpenFileName(
            self.centralWidget,
            'Abrir Imagem',
            '/home/cassiano/Imagens/',
            options = QFileDialog.DontUseNativeDialog

        )
        self.inputAbrirArquivo.setText(imagem)
        self.original_img = QPixmap(imagem)
        self.labelImg.setPixmap(self.original_img)

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    novo = Novo()
    novo.show()
    qt.exec_()


