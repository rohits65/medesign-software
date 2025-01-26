import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import os

class SensorFeedbackPage(QWidget):
    def __init__(self, app, workout_name):
        super().__init__()
        self.app = app
        self.workout_name = workout_name
        self.workouts = {
            "Workout 1": ["Warm-up: Jumping Jacks", "Squats", "Push-ups", "Cool down: Stretch"],
            "Workout 2": ["Warm-up: Light Jogging", "High Knees", "Burpees", "Cool down: Walk"],
            "Workout 3": ["Warm-up: Arm Circles", "Deadlifts", "Bench Press", "Cool down: Relax"],
        }
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2a2a2a; color: #ff9e5e;")
        layout = QVBoxLayout()

        title = QLabel(f"Sensor Feedback: {self.workout_name}")
        title.setFont(QFont("Arial", 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.steps_label = QLabel("Steps will appear here.")
        self.steps_label.setWordWrap(True)
        self.steps_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.steps_label)

        start_button = QPushButton("Start Workout")
        start_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        start_button.clicked.connect(self.start_workout)
        layout.addWidget(start_button)

        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        back_button.clicked.connect(self.go_to_home)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def start_workout(self):
        steps = self.workouts.get(self.workout_name, [])
        self.steps_label.setText("\n".join(steps))

    def go_to_home(self):
        self.app.central_widget.setCurrentWidget(self.app.home_page)

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

        workout_label = QLabel("Select a workout:")
        workout_label.setFont(QFont("Arial", 18))
        workout_label.setStyleSheet("color: #ff9e5e;")
        layout.addWidget(workout_label)

        workouts = ["Workout 1", "Workout 2", "Workout 3"]
        for workout in workouts:
            button = QPushButton(workout)
            button.setStyleSheet(
                "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
            )
            button.clicked.connect(lambda _, w=workout: self.app.open_sensor_feedback(w))
            layout.addWidget(button)

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

        title = QLabel("Workout Tutorials")
        title.setFont(QFont("Arial", 24))
        title.setStyleSheet("color: #ff7f32;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tutorials = ["Workout 1", "Workout 2", "Workout 3"]
        for tutorial in tutorials:
            button = QPushButton(f"Tutorial: {tutorial}")
            button.setStyleSheet(
                "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
            )
            button.clicked.connect(lambda _, t=tutorial: self.app.open_tutorial(t))
            layout.addWidget(button)

        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet(
            "background-color: #ff7f32; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        back_button.clicked.connect(lambda: self.app.central_widget.setCurrentWidget(self.app.home_page))
        layout.addWidget(back_button)

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

        back_button = QPushButton("Back to Tutorials")
        back_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        back_button.clicked.connect(lambda: self.app.central_widget.setCurrentWidget(self.app.tutorials_page))
        layout.addWidget(back_button)

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
