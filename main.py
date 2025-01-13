import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# page imports
from pages.home import create_home_page
from pages.history import create_stats_page
from pages.feedback import create_feedback_page
from pages.tutorial import create_tutorial_page

class WorkoutApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.appName = "Title"

        self.setWindowTitle(self.appName)
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create pages
        self.home_page = create_home_page(self)
        self.stats_page = create_stats_page(self)

        self.central_widget.addWidget(self.home_page)
        self.central_widget.addWidget(self.stats_page)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorkoutApp()
    window.show()
    sys.exit(app.exec_())
