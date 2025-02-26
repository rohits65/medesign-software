import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QDialog, QFormLayout, QSpinBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import os

def create_back_button(callback):
    back_button = QPushButton("Back")
    back_button.setStyleSheet(
        "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
    )
    back_button.clicked.connect(callback)
    return back_button

class SensorFeedbackPage(QWidget):
    def __init__(self, app, workout_name):
        super().__init__()
        self.app = app
        self.workout_name = workout_name
        self.workouts = {
            "Lat Pulldown": ["Step1", "Step2", "Step3", "Step4", "Step5"],
            "Lying Pullover": ["Step1", "Step2", "Step3", "Step4", "Step5"],
            "Seated Row": [
                "Sit down and grasp the handles.",
                "Keep your back straight and chest up.",
                "Pull the handles towards your torso.",
                "Pause briefly at the top of the movement.",
                "Slowly return to the starting position."
                ],
            "Kneeling Crunch": ["Step1", "Step2", "Step3", "Step4", "Step5"],
            "Face Pulls": ["Step1", "Step2", "Step3", "Step4", "Step5"],
        }
        self.current_step = 0
        self.reps = 1  # Default reps
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2a2a2a; color: #ff9e5e;")
        layout = QVBoxLayout()

        back_button = create_back_button(self.go_to_home)
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        title = QLabel(f"Sensor Feedback: {self.workout_name}")
        title.setFont(QFont("Arial", 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.steps_label = QLabel("Steps will appear here.")
        self.steps_label.setWordWrap(True)
        self.steps_label.setStyleSheet("font-size: 24px; margin-bottom: 5px;")
        self.steps_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.steps_label)

        self.feedback_label = QLabel("Feedback will appear here.")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setStyleSheet("font-size: 24px; margin-top: 5px;")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.feedback_label)

        settings_button = QPushButton("Workout Settings")
        settings_button.setStyleSheet(
            "background-color: #ff7f32; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        settings_button.clicked.connect(self.open_settings_dialog)
        layout.addWidget(settings_button)

        start_button = QPushButton("Start Workout")
        start_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        start_button.clicked.connect(self.start_workout)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def open_settings_dialog(self):
        dialog = WorkoutSettingsDialog(self)
        if dialog.exec_():
            self.reps = dialog.reps_input.value()

    def start_workout(self):
        self.current_step = 0
        self.reps_done = 0
        self.show_step()

    def show_step(self):
        steps = self.workouts.get(self.workout_name, [])
        if self.reps_done < self.reps:
            if self.current_step < len(steps):
                self.steps_label.setText(steps[self.current_step])
                self.current_step += 1
                QTimer.singleShot(2000, self.show_step)  # Show next step after 2 seconds
            else:
                self.reps_done += 1
                self.current_step = 0
                self.steps_label.setText(f"Cycle {self.reps_done} complete. Restarting...")
                QTimer.singleShot(2000, self.show_step)
        else:
            self.steps_label.setText("Workout complete!")

    def go_to_home(self):
        self.app.central_widget.setCurrentWidget(self.app.home_page)

class WorkoutSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Workout Settings")
        self.setStyleSheet("background-color: #2a2a2a; color: #ff9e5e;")
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.reps_input = QSpinBox()
        self.reps_input.setRange(1, 10)
        self.reps_input.setValue(1)
        self.reps_input.setStyleSheet("font-size: 16px;")
        layout.addRow("Number of Reps:", self.reps_input)

        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 5px; font-size: 14px; border-radius: 5px;"
        )
        buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet(
            "background-color: #ff7f32; color: #333333; padding: 5px; font-size: 14px; border-radius: 5px;"
        )
        buttons_layout.addWidget(cancel_button)

        layout.addRow(buttons_layout)
        self.setLayout(layout)

class HomePage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2a2a2a;")
        layout = QVBoxLayout()

        title = QLabel("Workout Options")
        title.setFont(QFont("Arial", 24))
        title.setStyleSheet("color: #ff7f32;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #2a2a2a; border: none;")

        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)
        scroll_widget.setLayout(scroll_layout)

        button_layout = QVBoxLayout()
        button_layout.addWidget(scroll_area)
        button_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(button_layout)

        workouts = ["Lat Pulldown",
            "Lying Pullover",
            "Seated Row",
            "Kneeling Crunch",
            "Face Pulls"
        ]
        
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for workout in workouts:
            button = QPushButton(workout)
            button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px; width: 250px"
            )
            button.clicked.connect(lambda _, w=workout: self.app.open_sensor_feedback(w))
            scroll_layout.addWidget(button)

        scroll_area.setWidget(scroll_widget)

        tutorials_button = QPushButton("Go to Tutorials")
        tutorials_button.setStyleSheet(
            "background-color: #ff7f32; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        tutorials_button.clicked.connect(self.app.open_tutorials_page)
        layout.addWidget(tutorials_button)

        self.setLayout(layout)

class TutorialsPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2a2a2a;")
        layout = QVBoxLayout()

        back_button = create_back_button(lambda: self.app.central_widget.setCurrentWidget(self.app.home_page))
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        title = QLabel("Workout Tutorials")
        title.setFont(QFont("Arial", 24))
        title.setStyleSheet("color: #ff7f32;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #2a2a2a; border: none;")

        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)
        scroll_widget.setLayout(scroll_layout)

        tutorials = ["Lat Pulldown",
            "Lying Pullover",
            "Seated Row",
            "Kneeling Crunch",
            "Face Pulls"
        ]
        for tutorial in tutorials:
            button = QPushButton(f"{tutorial}")
            button.setStyleSheet(
                "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
            )
            button.clicked.connect(lambda _, t=tutorial: self.app.open_tutorial(t))
            scroll_layout.addWidget(button)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

class TutorialPage(QWidget):
    def __init__(self, app, workout):
        super().__init__()
        self.app = app
        self.workout = workout
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2a2a2a;")
        layout = QVBoxLayout()

        back_button = create_back_button(lambda: self.app.central_widget.setCurrentWidget(self.app.tutorials_page))
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        title = QLabel(f"Tutorial for {self.workout}")
        title.setFont(QFont("Arial", 20))
        title.setStyleSheet("color: #ff7f32;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        video_widget = QVideoWidget()
        video_widget.setStyleSheet("border: 2px solid #ff7f32;")
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(video_widget)

        video_path = os.path.join("videos", f"{self.workout.lower().replace(' ', '_')}.mp4")
        if os.path.exists(video_path):
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
            self.media_player.play()
        else:
            error_label = QLabel("Video not found")
            error_label.setStyleSheet("color: #ff7f32;")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)

        layout.addWidget(video_widget)

        self.setLayout(layout)

class WorkoutApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Workout App")
        self.setStyleSheet("background-color: #2a2a2a;")
        self.resize(800, 600)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.home_page = HomePage(self)
        self.tutorials_page = TutorialsPage(self)

        self.central_widget.addWidget(self.home_page)
        self.central_widget.addWidget(self.tutorials_page)

    def open_sensor_feedback(self, workout_name):
        sensor_feedback_page = SensorFeedbackPage(self, workout_name)
        self.central_widget.addWidget(sensor_feedback_page)
        self.central_widget.setCurrentWidget(sensor_feedback_page)

    def open_tutorials_page(self):
        self.central_widget.setCurrentWidget(self.tutorials_page)

    def open_tutorial(self, workout):
        tutorial_page = TutorialPage(self, workout)
        self.central_widget.addWidget(tutorial_page)
        self.central_widget.setCurrentWidget(tutorial_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    workout_app = WorkoutApp()
    workout_app.show()
    sys.exit(app.exec_())
