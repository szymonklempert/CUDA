import sys
import cv2
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSlider, QHBoxLayout, QSplitter
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = None  # Variable to store the path of the loaded image
        self.output_path = None  # Variable to store the path of the output image
        self.last_filter_clicked = None  # Variable to store the last filter button clicked
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 1600, 900)  # Increase the width of the window

        self.layout = QHBoxLayout()

        self.splitter = QSplitter(QtCore.Qt.Horizontal)

        self.image_layout = QVBoxLayout()
        self.label = QLabel()
        self.image_layout.addWidget(self.label)

        self.button_load = QPushButton("Load Image")
        self.button_load.clicked.connect(self.load_image)
        self.image_layout.addWidget(self.button_load)

        self.label_output = QLabel()
        self.image_layout.addWidget(self.label_output)

        self.splitter.addWidget(QWidget())
        self.splitter.addWidget(QWidget())
        self.splitter.setSizes([self.width() // 2, self.width() // 2])

        self.splitter.widget(0).setLayout(self.image_layout)
        self.layout.addWidget(self.splitter)

        self.controls_layout = QVBoxLayout()

        self.slider_process = QSlider(QtCore.Qt.Horizontal)
        self.slider_process.setMinimum(0)
        self.slider_process.setMaximum(100)
        self.slider_process.valueChanged.connect(lambda value: self.update_label(self.label_process, value))
        self.slider_process.valueChanged.connect(lambda value: self.update_label(self.label_process, value))
        self.slider_process.valueChanged.connect(self.slider_run_filter)
        self.controls_layout.addWidget(self.slider_process)

        self.label_process = QLabel("Slider Value: 0")
        self.controls_layout.addWidget(self.label_process)

        self.button_process1 = QPushButton("Box filter")
        self.button_process1.clicked.connect(lambda: self.set_last_filter_clicked("box"))
        self.controls_layout.addWidget(self.button_process1)

        self.button_process2 = QPushButton("Laplacian filter")
        self.button_process2.clicked.connect(lambda: self.set_last_filter_clicked("laplacian"))
        self.controls_layout.addWidget(self.button_process2)


        self.button_process3 = QPushButton("Median filter")
        self.button_process3.clicked.connect(lambda: self.set_last_filter_clicked("median"))
        self.controls_layout.addWidget(self.button_process3)

        self.button_process4 = QPushButton("Sharpening filter")
        self.button_process4.clicked.connect(lambda: self.set_last_filter_clicked("sharpening"))
        self.controls_layout.addWidget(self.button_process4)

        self.button_process5 = QPushButton("Sobel filter")
        self.button_process5.clicked.connect(lambda: self.set_last_filter_clicked("sobel"))
        self.controls_layout.addWidget(self.button_process5)

        self.layout.addLayout(self.controls_layout)

        self.setLayout(self.layout)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)", options=options)
        if filename:
            self.image_path = filename  # Store the path of the loaded image
            image = cv2.imread(filename)
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, channel = image.shape
                bytesPerLine = 3 * width
                qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)
                self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio))
            else:
                print("Error: Unable to load image.")

    def set_last_filter_clicked(self, filter_name):
        self.last_filter_clicked = filter_name
        self.run_filter()

    def run_filter(self):
        if self.image_path and self.last_filter_clicked:
            input_file = self.image_path
            output_file = "output.jpg"  # Temporary output file name
            strength = str(self.slider_process.value())
            command = [f"{dir_path}/filter", self.last_filter_clicked, input_file, output_file, strength]
            print(command)

            try:
                subprocess.run(command, check=True)
                output_image = cv2.imread(output_file)
                self.show_output_image(output_image)
            except subprocess.CalledProcessError as e:
                print(f"Error running filter: {e}")
            finally:
                self.output_path = output_file

    def slider_run_filter(self):
        if self.last_filter_clicked in ["median", "sharpening"]:
            print("Median/sharpening filters do not support strength")
            return

        if self.image_path and self.last_filter_clicked:
            input_file = self.image_path
            output_file = "output.jpg"  # Temporary output file name
            strength = str(self.slider_process.value())
            command = [f"{dir_path}/filter", self.last_filter_clicked, input_file, output_file, strength]
            print(command)

            try:
                subprocess.run(command, check=True)
                output_image = cv2.imread(output_file)
                self.show_output_image(output_image)
            except subprocess.CalledProcessError as e:
                print(f"Error running filter: {e}")
            finally:
                self.output_path = output_file

    def show_output_image(self, image):
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            bytesPerLine = 3 * width
            qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.label_output.setPixmap(pixmap.scaled(self.label_output.size(), QtCore.Qt.KeepAspectRatio))

    def update_label(self, label, value):
        label.setText(f"Slider Value: {value}")

def main():
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
