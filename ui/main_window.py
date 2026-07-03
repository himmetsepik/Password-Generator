from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QSpinBox,
    QLineEdit,
    QMessageBox,
    QApplication,
    QProgressBar,
    QFrame
)
from PyQt6.QtCore import Qt, QTimer

from core.generator import generate_password, password_strength


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Generator")
        self.setFixedSize(560, 560)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(28, 28, 28, 28)

        self.card = QFrame()
        self.card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(32, 28, 32, 28)
        card_layout.setSpacing(16)

        title = QLabel("🔐 Password Generator")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        length_layout = QHBoxLayout()

        length_label = QLabel("Password Length:")
        length_label.setObjectName("label")

        self.length_input = QSpinBox()
        self.length_input.setMinimum(8)
        self.length_input.setMaximum(64)
        self.length_input.setValue(16)

        length_layout.addWidget(length_label)
        length_layout.addStretch()
        length_layout.addWidget(self.length_input)

        self.uppercase_check = QCheckBox("Uppercase Letters")
        self.lowercase_check = QCheckBox("Lowercase Letters")
        self.numbers_check = QCheckBox("Numbers")
        self.symbols_check = QCheckBox("Symbols")

        self.uppercase_check.setChecked(True)
        self.lowercase_check.setChecked(True)
        self.numbers_check.setChecked(True)
        self.symbols_check.setChecked(True)

        self.generate_button = QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.create_password)

        self.password_output = QLineEdit()
        self.password_output.setReadOnly(True)
        self.password_output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_output.setPlaceholderText("Generated password will appear here")

        self.strength_label = QLabel("Strength: -")
        self.strength_label.setObjectName("strengthLabel")
        self.strength_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.strength_bar = QProgressBar()
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setValue(0)

        self.copy_button = QPushButton("Copy Password")
        self.copy_button.clicked.connect(self.copy_password)

        card_layout.addWidget(title)
        card_layout.addSpacing(8)
        card_layout.addLayout(length_layout)
        card_layout.addWidget(self.uppercase_check)
        card_layout.addWidget(self.lowercase_check)
        card_layout.addWidget(self.numbers_check)
        card_layout.addWidget(self.symbols_check)
        card_layout.addSpacing(6)
        card_layout.addWidget(self.generate_button)
        card_layout.addWidget(self.password_output)
        card_layout.addWidget(self.strength_label)
        card_layout.addWidget(self.strength_bar)
        card_layout.addWidget(self.copy_button)

        self.card.setLayout(card_layout)
        main_layout.addWidget(self.card)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f0f;
                color: #ffffff;
                font-family: Arial;
                font-size: 15px;
            }

            QFrame#card {
                background-color: #171717;
                border: 1px solid #2f2f2f;
                border-radius: 16px;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#title {
                color: #ffffff;
                font-size: 26px;
                font-weight: bold;
            }

            QLabel#label {
                color: #ffffff;
                font-size: 15px;
                font-weight: bold;
            }

            QLabel#strengthLabel {
                color: #ffffff;
                font-size: 15px;
                font-weight: bold;
            }

            QSpinBox {
                background-color: #222222;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                min-width: 180px;
                min-height: 36px;
                padding-left: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QSpinBox:hover {
                border: 1px solid #2563eb;
            }

            QCheckBox {
                background-color: transparent;
                color: #ffffff;
                font-size: 15px;
                spacing: 10px;
                padding: 4px 0;
            }

            QLineEdit {
                background-color: #222222;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                min-height: 42px;
                padding: 0 12px;
                font-size: 16px;
                font-weight: bold;
            }

            QLineEdit:hover {
                border: 1px solid #2563eb;
            }

            QLineEdit::placeholder {
                color: #9ca3af;
            }

            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 9px;
                min-height: 44px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3b82f6;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }

            QPushButton:disabled {
                background-color: #1e40af;
                color: #dbeafe;
            }

            QProgressBar {
                background-color: #222222;
                border: 1px solid #3a3a3a;
                border-radius: 7px;
                min-height: 14px;
                max-height: 14px;
            }

            QProgressBar::chunk {
                background-color: #2563eb;
                border-radius: 6px;
            }
        """)

    def create_password(self):
        try:
            password = generate_password(
                length=self.length_input.value(),
                use_uppercase=self.uppercase_check.isChecked(),
                use_lowercase=self.lowercase_check.isChecked(),
                use_numbers=self.numbers_check.isChecked(),
                use_symbols=self.symbols_check.isChecked()
            )

            self.password_output.setText(password)

            strength = password_strength(password)
            self.update_strength(strength)

        except ValueError as error:
            QMessageBox.warning(self, "Warning", str(error))

    def update_strength(self, strength):
        if strength == "Weak":
            self.strength_label.setText("Strength: Weak")
            self.strength_label.setStyleSheet("color: #ef4444; font-size: 15px; font-weight: bold;")
            self.strength_bar.setValue(33)
            color = "#ef4444"

        elif strength == "Medium":
            self.strength_label.setText("Strength: Medium")
            self.strength_label.setStyleSheet("color: #f59e0b; font-size: 15px; font-weight: bold;")
            self.strength_bar.setValue(66)
            color = "#f59e0b"

        else:
            self.strength_label.setText("Strength: Strong")
            self.strength_label.setStyleSheet("color: #22c55e; font-size: 15px; font-weight: bold;")
            self.strength_bar.setValue(100)
            color = "#22c55e"

        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #222222;
                border: 1px solid #3a3a3a;
                border-radius: 7px;
                min-height: 14px;
                max-height: 14px;
            }}

            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)

    def copy_password(self):
        password = self.password_output.text()

        if not password:
            QMessageBox.warning(self, "Warning", "Please generate a password first.")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(password)

        self.copy_button.setText("Copied ✓")
        self.copy_button.setEnabled(False)

        QTimer.singleShot(1200, self.reset_copy_button)

    def reset_copy_button(self):
        self.copy_button.setText("Copy Password")
        self.copy_button.setEnabled(True)