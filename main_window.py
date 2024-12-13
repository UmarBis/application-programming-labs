import sys
import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QSizePolicy, QMessageBox
)

from img_iterator import ImageIterator


class ImageViewer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setFixedSize(QSize(1280, 700))

        self.dataset_iterator = None
        self.current_image_path = None

        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Set up the user interface.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.image_label = QLabel("CHOOSE CSV FILE", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet(
            "background-color: slategrey; border: 2px solid #adaaaa; border-radius: 5px;"
        )
        layout.addWidget(self.image_label)

        self.load_dataset_button = QPushButton("Load Dataset")
        self.load_dataset_button.setFixedSize(1000, 50)
        self.load_dataset_button.setStyleSheet(
            "border: 2px solid #ababab; border-radius: 5px; background-color: darkgray;"
        )
        self.load_dataset_button.clicked.connect(self.load_dataset)
        layout.addWidget(self.load_dataset_button, alignment=Qt.AlignHCenter)

        self.next_image_button = QPushButton("Next Image")
        self.next_image_button.setFixedSize(1000, 50)
        self.next_image_button.setStyleSheet(
            "border: 2px solid #ababab; border-radius: 5px; background-color: darkgray;"
        )
        self.next_image_button.clicked.connect(self.show_next_image)
        self.next_image_button.setEnabled(False)
        layout.addWidget(self.next_image_button, alignment=Qt.AlignHCenter)

    def load_dataset(self) -> None:
        """
        Open a CSV file and initialize the dataset iterator.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Dataset Annotation File", "", "CSV Files (*.csv)"
        )
        if file_path:
            try:
                self.dataset_iterator = iter(ImageIterator(file_path))
                self.next_image_button.setEnabled(True)
                self.show_next_image()  # Отображение первого изображения
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading dataset: {e}")

    def show_next_image(self) -> None:
        """
        Show the next image from the dataset iterator.
        """
        if self.dataset_iterator:
            try:
                self.current_image_path = next(self.dataset_iterator)[0]
                if os.path.exists(self.current_image_path):
                    self.display_image(self.current_image_path)
                else:
                    QMessageBox.warning(
                        self, "File Not Found", f"Image not found: {self.current_image_path}"
                    )
            except StopIteration:
                QMessageBox.information(self, "End of Dataset", "No more images in the dataset.")
                self.next_image_button.setEnabled(False)

    def display_image(self, image_path: str) -> None:
        """
        Display the image in QLabel.
        :param: path to the image file.
        """
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                QMessageBox.critical(self, "Error", "Invalid image file.")
            else:
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error displaying image: {e}")


def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
