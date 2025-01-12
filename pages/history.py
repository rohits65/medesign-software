import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

def create_stats_page(app):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Your PT Stats")
        label.setFont(QFont("Arial", 20))
        label.setStyleSheet("color: orange;")
        label.setAlignment(Qt.AlignCenter)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet("background-color: orange; color: black; padding: 10px; font-size: 16px;")
        back_btn.clicked.connect(lambda: app.central_widget.setCurrentWidget(app.home_page))

        layout.addWidget(label)
        layout.addWidget(back_btn)

        layout.setAlignment(Qt.AlignCenter)
        page.setLayout(layout)
        page.setStyleSheet("background-color: black;")

        return page