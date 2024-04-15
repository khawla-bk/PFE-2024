import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QTimer

# Simulated sensor data
tank_data = {
    "tank1": 70,
    "tank2": 50,
    "tank3": 80
}

class TankLevelMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tank Level Monitor")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.progressbars = {}

        for tank, level in tank_data.items():
            progressbar = QProgressBar()
            progressbar.setRange(0, 100)  # Tank level ranges from 0% to 100%
            progressbar.setValue(level)  # Set initial tank level
            self.layout.addWidget(progressbar)
            self.progressbars[tank] = progressbar

        # Update tank levels periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_levels)
        self.timer.start(1000)  # Update every second

    def update_levels(self):
        # Simulated sensor data update
        for tank, level in tank_data.items():
            tank_data[tank] = (level + 1) % 101  # Increment tank level cyclically
            self.progressbars[tank].setValue(tank_data[tank])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tank_monitor = TankLevelMonitor()
    tank_monitor.show()
    sys.exit(app.exec_())