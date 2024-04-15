import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import QRectF, Qt, QPointF, QLineF
import math

class CircularGauge(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuel Tank Level")
        self.setMinimumSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fixed center coordinates
        center_x = self.width() / 2
        center_y = self.height() / 2

        # Define gauge parameters
        outer_radius = min(self.width(), self.height()) / 2 - 10
        start_angle = 180  # Start angle in degrees
        end_angle = 0  # End angle in degrees
        range_degrees = end_angle - start_angle


        # Define angle ranges and corresponding colors
        angle_ranges = [(0, 46), (46, 91), (91, 136), (136, 181)]
        colors = ["#94C816", "#EBA104", "#E4670B", "#BA1301"]

        # Draw graduations on the arc
        num_graduations = 4  # Number of graduations
        graduation_length = 8  # Length of graduation lines
        # Draw arc with graduations
        for angle_range, color in zip(angle_ranges, colors):
            angle_start, angle_end = angle_range
            angle = (angle_start + angle_end) / 2  # Calculate the angle for text placement
            painter.setPen(QPen(QColor(color), 20))
            painter.drawArc(QRectF(center_x - outer_radius, center_y - outer_radius, outer_radius * 2, outer_radius * 2),
                            angle_start * 16, (angle_end - angle_start) * 16)

            
            """# Calculate angle for each graduation
            angle = start_angle +  * range_degrees / num_graduations

            # Calculate start and end points for graduation lines
            start_point = QPointF(center_x + outer_radius * math.cos(math.radians(angle)),
                                    center_y - outer_radius * math.sin(math.radians(angle)))
            end_point = QPointF(center_x + (outer_radius - graduation_length) * math.cos(math.radians(angle)),
                                    center_y - (outer_radius - graduation_length) * math.sin(math.radians(angle)))

            # Draw graduation line
            painter.drawLine(start_point, end_point)"""

        """# Draw start and end values of the arc
        start_point = QPointF(center_x + outer_radius * math.cos(math.radians(angle)),center_y - outer_radius * math.sin(math.radians(angle)))
        end_point = QPointF(center_x + (outer_radius - graduation_length) * math.cos(math.radians(angle)),center_y - (outer_radius - graduation_length) * math.sin(math.radians(angle)))
        painter.drawText(center_x, "0%")
        painter.drawText(center_y, "100% ") """

        font = QFont("Arial", 20)
        painter.setFont(font)
        painter.setPen(QColor("#000000"))
        # Draw needle at the center of the arc
        value = 75  # Example value (change as needed)
        needle_angle = start_angle + (value / 100) * range_degrees  # Calculate needle angle based on value
        needle_length = outer_radius - 30
        needle_line = QLineF(center_x, center_y, center_x + needle_length * math.cos(math.radians(needle_angle)),
                                                  center_y - needle_length * math.sin(math.radians(needle_angle)))
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(needle_line)

        # Draw value of the tank under the gauge
        painter.drawText(240,300, "Tank Value: {}%".format(value))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gauge = CircularGauge()
    gauge.show()
    sys.exit(app.exec_())
