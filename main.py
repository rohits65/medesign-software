import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QScrollBar, QLineEdit, QSpinBox, QDialog, 
    QFormLayout, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt


class SensorFeedbackPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        
        self.current_step = 0
        self.reps_completed = 0
        self.reps = 0
        self.workouts = {
            "Full Body": {
                "steps": ["Warm-up: Jumping Jacks", "Squats", "Push-ups", "Cool down: Stretch"],
                "reps": 3,
            },
            "Cardio": {
                "steps": ["Warm-up: Light Jogging", "High Knees", "Burpees", "Cool down: Walk"],
                "reps": 5,
            },
            "Strength": {
                "steps": ["Warm-up: Arm Circles", "Deadlifts", "Bench Press", "Cool down: Relax"],
                "reps": 4,
            },
        }
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2a2a2a; color: #ff9e5e;")
        layout = QVBoxLayout()

        # Title
        title = QLabel("Sensor Data & Feedback")
        title.setFont(QFont("Arial", 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Labels for sensor data and feedback
        self.sensor_data_label = QLabel("Heart Rate: -- BPM")
        self.sensor_data_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.sensor_data_label)

        self.feedback_label = QLabel("Select a workout to start.")
        self.feedback_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.feedback_label)

        self.steps_label = QLabel("Steps will appear here.")
        self.steps_label.setWordWrap(True)
        self.steps_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.steps_label)

        # Workout selection dropdown
        self.workout_selector = QComboBox()
        self.workout_selector.addItems(self.workouts.keys())
        self.workout_selector.setStyleSheet("font-size: 16px; padding: 5px;")
        layout.addWidget(self.workout_selector)

        # Buttons
        start_button = QPushButton("Start Workout")
        start_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        start_button.clicked.connect(self.start_workout)
        layout.addWidget(start_button)

        back_button = QPushButton("Back to Tutorial")
        back_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        back_button.clicked.connect(self.go_to_tutorial)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def start_workout(self):
        selected_workout = self.workout_selector.currentText()
        workout = self.workouts[selected_workout]
        self.steps = workout["steps"]
        self.reps = workout["reps"]
        self.current_step = 0
        self.reps_completed = 0
        self.steps_label.setText("")
        self.feedback_label.setText(f"Starting '{selected_workout}' workout: {self.reps} reps")
        self.start_cycle()

    def start_cycle(self):
        if self.reps_completed >= self.reps:
            self.feedback_label.setText("Workout complete! Great job!")
            return

        self.display_step()

    def display_step(self):
        if self.current_step < len(self.steps):
            self.steps_label.setText(f"Step {self.current_step + 1}: {self.steps[self.current_step]}")
            self.current_step += 1
            QTimer.singleShot(2000, self.display_step)  # Show next step after 2 seconds
        else:
            self.reps_completed += 1
            self.current_step = 0
            self.feedback_label.setText(f"Cycle completed! Reps done: {self.reps_completed}/{self.reps}")
            QTimer.singleShot(3000, self.start_cycle)  # Start next cycle after 3 seconds

    def go_to_tutorial(self):
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

        # Scrollable horizontal workout list
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)

        workout_list_widget = QWidget()
        workout_list_layout = QHBoxLayout()

        workouts = ["Workout 1", "Workout 2", "Workout 3", "Workout 4", "Workout 5"]
        for workout in workouts:
            button = QPushButton(workout)
            button.setStyleSheet(
                "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
            )
            button.clicked.connect(lambda _, w=workout: self.app.open_tutorial(w))
            workout_list_layout.addWidget(button)

        workout_list_widget.setLayout(workout_list_layout)
        scroll_area.setWidget(workout_list_widget)
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

        button_layout = QVBoxLayout()

        next_button = QPushButton("Next")
        next_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        next_button.clicked.connect(self.go_to_sensor_feedback)
        button_layout.addWidget(next_button)

        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            "background-color: #ff9e5e; color: #333333; padding: 10px; font-size: 16px; border-radius: 5px;"
        )
        back_button.clicked.connect(self.go_to_home)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def go_to_home(self):
        self.app.central_widget.setCurrentWidget(self.app.home_page)

    def go_to_sensor_feedback(self):
        sensor_feedback_page = SensorFeedbackPage(self.app)
        self.app.central_widget.addWidget(sensor_feedback_page)
        self.app.central_widget.setCurrentWidget(sensor_feedback_page)

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
        self.central_widget.addWidget(self.home_page)

    def open_tutorial(self, workout):
        tutorial_page = TutorialPage(self, workout)
        self.central_widget.addWidget(tutorial_page)
        self.central_widget.setCurrentWidget(tutorial_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    workout_app = WorkoutApp()
    workout_app.show()
    sys.exit(app.exec_())
