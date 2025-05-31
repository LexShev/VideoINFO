from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QProgressBar, QPushButton, QDialog, QDialogButtonBox


class SingleProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Processing...")
        self.setWindowModality(Qt.WindowModal)
        self.setFixedSize(650, 150)
        self.setStyleSheet(
            "QPushButton {color: white; background-color:rgba(255,255,255,30);"
            "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
            "QPushButton:hover {background-color:rgba(255,255,255,50);}"
            "QPushButton:pressed{background-color:rgba(255,255,255,70);}"
        )
        layout = QVBoxLayout(self)
        self.label = QLabel('Start scan')
        self.label.setAlignment(Qt.AlignCenter)

        self.single_progress_bar = QProgressBar()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(70, 30)

        layout.addWidget(self.label)
        layout.addWidget(self.single_progress_bar)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)


class DoubleProgressDialog(QDialog):
    def  __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Processing...")
        self.setWindowModality(Qt.WindowModal)
        self.setFixedSize(650, 200)
        self.setStyleSheet(
            "QPushButton {color: white; background-color:rgba(255,255,255,30);"
            "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
            "QPushButton:hover {background-color:rgba(255,255,255,50);}"
            "QPushButton:pressed{background-color:rgba(255,255,255,70);}"
        )

        # Создаем layout
        layout = QVBoxLayout(self)

        # Первый прогрессбар с меткой
        self.label_01 = QLabel("Current task:")
        self.label_01.setAlignment(Qt.AlignCenter)
        self.progress_01 = QProgressBar()

        # Второй прогрессбар с меткой
        self.label_02 = QLabel("Total progress:")
        self.label_02.setAlignment(Qt.AlignCenter)
        self.progress_02 = QProgressBar()

        # Кнопка отмены
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(70, 30)

        # self.cancel_button.clicked.connect(self.reject)

        # Добавляем виджеты в layout
        layout.addWidget(self.label_01)
        layout.addWidget(self.progress_01)
        layout.addWidget(self.label_02)
        layout.addWidget(self.progress_02)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)

        # Настройка прогрессбаров
        self.progress_01.setRange(0, 100)
        self.progress_02.setRange(0, 100)


class CustomDialog(QDialog):
    def __init__(self, message_text):
        super().__init__()

        self.setWindowTitle("Attention!")

        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(message_text)
        message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class AttentionDialog(QDialog):
    def __init__(self, title, message_text):
        super().__init__()

        self.setWindowTitle(title)
        qbtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(message_text)
        message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)