import sys

import PyQt5
from PyQt5.QtWidgets import QVBoxLayout, QToolBar, QWidget, QPlainTextEdit, QMainWindow, QAction, QApplication, \
    QFileDialog
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5 import uic

from GUI.Texto.Highlighter import Highlighter
from GUI.Texto.PlainTextEdit import PlainTextEdit

import Hardware.Hardware as machine

from Interpreter.BasicExecute import BasicLexer, BasicParser, BasicExecute
import threading

#Crear ejecutable
#pyinstaller --windowed --onefile main.py
#pyinstaller --windowed --onefile --icon=./GUI/imagenes/WindowIcon.png main.py



class MainWindow(QMainWindow):
    ruta = ""

    def __init__(self):
        super().__init__()

        # Se crea la ventana
        QMainWindow.__init__(self)
        uic.loadUi("GUI/mainwindow.ui", self)

        # Se definen las caracteristicas de la ventana
        self.setWindowTitle("Writting Machine IDE")
        self.setStyleSheet("background-color: #252525; color: white;")
        self.setWindowIcon(PyQt5.QtGui.QIcon("GUI/imagenes/WindowIcon.png"))
        self.setMinimumSize(600, 400)

        # Se crea una barra de acciones
        toolBar = QToolBar()
        toolBar.setStyleSheet("background-color: #707070; color: white;")

        # Se crea una lista de acciones
        abrir = QAction("Abrir", self)
        guardar = QAction("Guardar", self)
        guardarComo = QAction("Guardar como...", self)
        run = QAction("Run", self)
        stop = QAction("Stop", self)
        close = QAction("Exit", self)
        compilar = QAction("Compilar", self)

        # Se añaden los iconos de las acciones a la barra de acciones
        abrir.setIcon(PyQt5.QtGui.QIcon("GUI/imagenes/Open.png"))
        guardar.setIcon(PyQt5.QtGui.QIcon("GUI/imagenes/Save.png"))
        guardarComo.setIcon(PyQt5.QtGui.QIcon("GUI/imagenes/SaveAs.png"))
        run.setIcon(PyQt5.QtGui.QIcon("GUI/imagenes/Run.png"))
        stop.setIcon(PyQt5.QtGui.QIcon("GUI/imagenes/Stop.png"))
        close.setIcon(PyQt5.QtGui.QIcon("GUI/imagenes/Close.png"))
        compilar.setIcon(PyQt5.QtGui.QIcon("GUI/imagenes/Compile.png"))



        # Se definen las acciones de la barra de acciones
        abrir.triggered.connect(lambda: self.abrir(codeInput))
        guardar.triggered.connect(lambda: self.guardar(codeInput))
        guardarComo.triggered.connect(lambda: self.guardarComo(codeInput))
        run.triggered.connect(lambda: self.run(codeInput))
        stop.triggered.connect(lambda: self.stop(codeInput))
        close.triggered.connect(lambda: self.closeApp(codeInput))
        compilar.triggered.connect(lambda: self.compilar(codeInput))

        # Se agrega las acciones creadas a la barra de acciones
        toolBar.addAction(abrir)
        toolBar.addAction(guardar)
        toolBar.addAction(guardarComo)
        toolBar.addAction(run)
        toolBar.addAction(stop)
        toolBar.addAction(close)
        toolBar.addAction(compilar)

        # Se agrega la barra de acciones a la ventana
        self.addToolBar(toolBar)

        # =======================================================================================================================

        # Se define un layout para los widgets
        layout = QVBoxLayout(self)

        # Se define un cuadro de texto para ingresar código
        code = QPlainTextEdit(self)
        code.hide()
        codeInput = PlainTextEdit(code)
        codeInput.setStyleSheet("background-color: #551641; color: white;")

        # Se definen las plabras que serán resaltadas en el cuadro de texto
        self.highlighter = Highlighter(codeInput.document())

        # Se define un cuadro de texto para mostrar el resultado
        codeOutput = QPlainTextEdit(self)
        codeOutput.setStyleSheet("background-color: #551641; color: white;")
        codeOutput.setReadOnly(True)

        # Se agregan los widgets al layout
        for widget in [codeInput, codeOutput]:
            layout.addWidget(widget)

        # Se define un widget para contener al layout
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Muestra la ventana
        self.show()

    def abrir(self, codeInput):

        # Se abre un cuadro de dialogo para seleccionar el archivo
        archivo = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "*.txt")

        if archivo[0]:
            # Se abre el archivo seleccionado
            with open(archivo[0], "r") as f:
                # Se lee el archivo
                codeInput.setPlainText(f.read())

            # Se guarda la ruta del archivo
            self.ruta = archivo[0]

    def guardar(self, codeInput):

        # Verifica si la ruta esta vacia
        if self.ruta == "":
            # Si la ruta esta vacia, se abre un cuadro de dialogo para guardar el archivo
            self.guardarComo(codeInput)
        else:
            # Si la ruta no esta vacia, se guarda el archivo en la ruta
            with open(self.ruta, "w") as f:
                f.write(codeInput.toPlainText())

    def guardarComo(self, codeInput):

        # Se abre un cuadro de dialogo para guardar el archivo
        fileName, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "Text Files (*.txt)")

        # Se verifica que no se haya cancelado el cuadro de dialogo
        if fileName != "":
            # Si el archivo no esta vacio, se guarda el archivo en la ruta
            with open(fileName, "w") as f:
                f.write(codeInput.toPlainText())

    def run(self, codeInput):
        t1 = threading.Thread(target=self.run_thread, args=(codeInput.toPlainText(),))
        t1.start()

    def run_thread(self, codeInput):
        # lexer = BasicLexer()
        # env = {}
        #
        # text = codeInput
        #
        # if text:
        #     lex = lexer.tokenize(text)
        #     try:
        #         for token in lex:
        #             print(token)
        #     except EOFError:
        #         print("EOF")



        # lexer = BasicLexer()
        # parser = BasicParser()
        # env = {}
        #
        # text = codeInput
        #
        #
        # text = codeInput + "\n" + "MAIN();"
        #
        # text = text + "\n" + "Up;" + "\n"+"Beginning;"
        #
        # if text:
        #     tree = parser.parse(lexer.tokenize(text))
        #     print(tree)



        lexer = BasicLexer()
        parser = BasicParser()
        varDictionary = {}
        funDictionary = {}

        execute = BasicExecute(varDictionary, funDictionary)
        lastTree = None

        if "MAIN();" in codeInput:
            text = codeInput
        else:
            text = codeInput + "\n" + "MAIN();"
        text = text + "\n" + "Up;" + "\n" + "Beginning;"

        if text:
            tree = parser.parse(lexer.tokenize(text))
            execute.startExecute(tree, lastTree, varDictionary, funDictionary)
            lastTree = tree




    def stop(self, codeInput):
        print("Stop")

    def closeApp(self, codeInput):
        self.close()
        # print("Close")

    def compilar(self, codeInput):

        t1 = threading.Thread(target=self.compilar_thread, args=(codeInput.toPlainText(),))
        t1.start()

    def compilar_thread(self, codeInput):
        lexer = BasicLexer()
        parser = BasicParser()
        varDictionary = {}
        funDictionary = {}

        execute = BasicExecute(varDictionary, funDictionary)
        lastTree = None

        text = codeInput
        textsplit = text.split("\n")


        print(textsplit)
        for line in textsplit:
            if line:
                tree = parser.parse(lexer.tokenize(line))
                execute.startExecute(tree, lastTree, varDictionary, funDictionary)
                lastTree = tree
                # lex = lexer.tokenize(text)
                # for token in lex:
                #     print(token)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
