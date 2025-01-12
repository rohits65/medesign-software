from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

def create_home_page(app):
    page = QWidget()
    layout = QVBoxLayout()

    label = QLabel("Welcome to " + app.appName)
    label.setFont(QFont("Arial", 20))
    label.setStyleSheet("color: orange;")
    label.setAlignment(Qt.AlignCenter)

    stats_btn = QPushButton("View Progress")
    stats_btn.setStyleSheet("background-color: orange; color: black; padding: 10px; font-size: 16px;")
    stats_btn.clicked.connect(lambda: app.central_widget.setCurrentWidget(app.stats_page))

    layout.addWidget(label)
    layout.addWidget(stats_btn)

    layout.setAlignment(Qt.AlignCenter)
    page.setLayout(layout)
    page.setStyleSheet("background-color: black;")

    return page

