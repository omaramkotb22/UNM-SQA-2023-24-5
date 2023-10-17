import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSplitter, QVBoxLayout
from PyQt5.QtCore import Qt

class SplitWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()  # Create a vertical layout for the central widget
        central_widget.setLayout(central_layout)  # Set the layout for the central widget

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget(splitter)
        right_widget = QWidget(splitter)

        left_widget.setStyleSheet("background-color: lightblue")
        left_widget.setMinimumWidth(200)

        right_widget.setStyleSheet("background-color: lightgray")

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([200, 600])

        # Add the splitter to the central layout
        central_layout.addWidget(splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitWindow()
    window.showMaximized() 
    sys.exit(app.exec_())
