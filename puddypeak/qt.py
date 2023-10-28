from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        button = QPushButton("Press me!")

        self.setCentralWidget(button)
# Create a Qt widget, which will be our window.
# window = QWidget()
# window = QPushButton("Push Me")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

# Start the event loop.
app.exec()
