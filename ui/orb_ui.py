from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QBrush, QRadialGradient
import sys

class AnimatedOrb(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectra")
        self.setGeometry(100, 100, 200, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.orb_size = 100
        self.center = QPoint(self.orb_size, self.orb_size)
        self.color = QColor(0, 150, 255)  # Blue tone
        self.pulsating = False
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # Update every 50ms
        
        self.animation_phase = 0
        
    def update_animation(self):
        if self.pulsating:
            self.animation_phase = (self.animation_phase + 0.1) % (2 * 3.14159)
            self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate pulse effect
        pulse = 1.0
        if self.pulsating:
            pulse = 1.0 + 0.2 * abs(float(self.animation_phase) - 3.14159) / 3.14159
        
        size = self.orb_size * pulse
        
        # Create gradient
        gradient = QRadialGradient(self.center, size)
        gradient.setColorAt(0, self.color.lighter(150))
        gradient.setColorAt(0.7, self.color)
        gradient.setColorAt(1, self.color.darker(150))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.center, size, size)
    
    def set_listening_state(self, listening):
        """Change orb appearance based on state"""
        self.pulsating = listening
        if listening:
            self.color = QColor(0, 200, 0)  # Green when listening
        else:
            self.color = QColor(0, 150, 255)  # Blue when idle
        self.update()
    
    def mousePressEvent(self, event):
        """Allow dragging the orb"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()