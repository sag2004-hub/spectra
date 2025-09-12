from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QRectF
from PyQt5.QtGui import QColor, QPainter, QBrush, QRadialGradient, QFont, QPen, QLinearGradient, QPolygonF
import sys
import math
import random

class AnimatedOrb(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectra AI")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Enhanced size for JARVIS-like appearance
        self.window_size = 350
        self.orb_size = 120
        self.setFixedSize(self.window_size, self.window_size)
        
        # Center the window on screen
        self.center_on_screen()
        
        self.center = QPoint(self.window_size // 2, self.window_size // 2)
        self.color = QColor(0, 150, 255)  # Blue tone
        self.pulsating = False
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # Update every 50ms
        
        self.animation_phase = 0
        self.sparkle_phase = 0
        self.ring_phase = 0
        
        # Initialize sparkle positions around the text
        self.sparkles = []
        for i in range(16):  # More sparkles for JARVIS effect
            angle = (i * 22.5) * (math.pi / 180)  # 22.5-degree intervals
            radius = random.randint(40, 80)
            self.sparkles.append({
                'angle': angle,
                'radius': radius,
                'phase': random.random() * 2 * math.pi,
                'speed': random.uniform(0.03, 0.12),
                'brightness': random.uniform(0.4, 1.0),
                'size': random.uniform(2, 5)
            })
        
        # Initialize rotating rings for JARVIS effect
        self.rings = []
        for i in range(3):
            self.rings.append({
                'radius': 90 + (i * 25),
                'width': 2,
                'speed': 0.02 + (i * 0.01),
                'phase': i * (2 * math.pi / 3),
                'segments': 8 + (i * 4)
            })
    
    def center_on_screen(self):
        """Center the window on the screen"""
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry()
        window_rect = self.geometry()
        
        x = (screen_rect.width() - window_rect.width()) // 2
        y = (screen_rect.height() - window_rect.height()) // 2
        
        self.move(x, y)
        
    def update_animation(self):
        self.animation_phase = (self.animation_phase + 0.08) % (2 * math.pi)
        self.sparkle_phase = (self.sparkle_phase + 0.06) % (2 * math.pi)
        self.ring_phase = (self.ring_phase + 0.04) % (2 * math.pi)
        
        # Update sparkle phases
        for sparkle in self.sparkles:
            sparkle['phase'] = (sparkle['phase'] + sparkle['speed']) % (2 * math.pi)
            # Randomly change brightness for twinkling effect
            if random.random() < 0.08:  # 8% chance each frame
                sparkle['brightness'] = random.uniform(0.4, 1.0)
        
        # Update ring phases
        for ring in self.rings:
            ring['phase'] = (ring['phase'] + ring['speed']) % (2 * math.pi)
        
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        # Calculate pulse effect
        pulse = 1.0
        if self.pulsating:
            pulse = 1.0 + 0.25 * (math.sin(self.animation_phase) * 0.5 + 0.5)
        
        size = self.orb_size * pulse
        
        # Draw JARVIS-style rotating rings
        self.draw_jarvis_rings(painter)
        
        # Create outer glow with multiple layers
        for i in range(3):
            glow_radius = size * (1.8 - i * 0.2)
            glow_gradient = QRadialGradient(self.center, glow_radius)
            glow_color = QColor(self.color)
            glow_color.setAlpha(15 - i * 3)
            glow_gradient.setColorAt(0, glow_color)
            glow_color.setAlpha(0)
            glow_gradient.setColorAt(1, glow_color)
            
            painter.setBrush(QBrush(glow_gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.center, glow_radius, glow_radius)
        
        # Create main orb gradient with enhanced depth
        gradient = QRadialGradient(self.center, size)
        gradient.setColorAt(0, self.color.lighter(250))
        gradient.setColorAt(0.2, self.color.lighter(150))
        gradient.setColorAt(0.5, self.color.lighter(110))
        gradient.setColorAt(0.8, self.color)
        gradient.setColorAt(1, self.color.darker(180))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.center, size, size)
        
        # Add multiple inner highlights for depth
        highlight_positions = [
            (0.15, 0.15, 0.4),
            (0.25, 0.25, 0.25)
        ]
        
        for hx, hy, hs in highlight_positions:
            highlight_size = size * hs
            highlight_center = QPoint(
                self.center.x() - size * hx, 
                self.center.y() - size * hy
            )
            highlight_gradient = QRadialGradient(highlight_center, highlight_size)
            highlight_color = QColor(255, 255, 255, 80)
            highlight_gradient.setColorAt(0, highlight_color)
            highlight_color.setAlpha(0)
            highlight_gradient.setColorAt(1, highlight_color)
            
            painter.setBrush(QBrush(highlight_gradient))
            painter.drawEllipse(highlight_center, highlight_size, highlight_size)
        
        # Draw sparkles around the text area
        self.draw_sparkles(painter)
        
        # Draw the "Spectra" text with gradient and glow
        self.draw_spectra_text(painter)
        
        # Draw status indicator
        self.draw_status_indicator(painter)
    
    def draw_jarvis_rings(self, painter):
        """Draw rotating rings like JARVIS interface"""
        painter.setPen(Qt.NoPen)
        
        for ring in self.rings:
            ring_color = QColor(self.color)
            ring_color.setAlpha(40 if not self.pulsating else 80)
            
            # Draw segmented ring
            segment_angle = (2 * math.pi) / ring['segments']
            
            for i in range(ring['segments']):
                start_angle = (i * segment_angle) + ring['phase']
                
                # Vary segment brightness
                brightness = 0.3 + 0.7 * (math.sin(start_angle + self.ring_phase) * 0.5 + 0.5)
                segment_color = QColor(ring_color)
                segment_color.setAlpha(int(segment_color.alpha() * brightness))
                
                # Create segment gradient
                inner_radius = ring['radius'] - ring['width']
                outer_radius = ring['radius'] + ring['width']
                
                # Draw arc segment
                painter.setBrush(QBrush(segment_color))
                
                # Create polygon for ring segment
                points = []
                arc_length = segment_angle * 0.8  # Gap between segments
                
                for angle_step in range(8):
                    angle = start_angle + (angle_step * arc_length / 7)
                    inner_x = self.center.x() + inner_radius * math.cos(angle)
                    inner_y = self.center.y() + inner_radius * math.sin(angle)
                    outer_x = self.center.x() + outer_radius * math.cos(angle)
                    outer_y = self.center.y() + outer_radius * math.sin(angle)
                    
                    if angle_step < 4:
                        points.append(QPoint(int(inner_x), int(inner_y)))
                    if angle_step >= 4:
                        points.append(QPoint(int(outer_x), int(outer_y)))
                
                if points:
                    polygon = QPolygonF(points)
                    painter.drawPolygon(polygon)
    
    def draw_sparkles(self, painter):
        """Draw animated sparkles around the text"""
        painter.setPen(Qt.NoPen)
        
        for sparkle in self.sparkles:
            # Calculate sparkle position with orbital motion
            orbit_radius = sparkle['radius'] + 10 * math.sin(sparkle['phase'] * 0.5)
            x = self.center.x() + orbit_radius * math.cos(sparkle['angle'] + sparkle['phase'] * 0.3)
            y = self.center.y() + orbit_radius * math.sin(sparkle['angle'] + sparkle['phase'] * 0.3)
            
            # Create sparkle brightness based on phase and random brightness
            brightness = sparkle['brightness'] * (math.sin(sparkle['phase']) * 0.4 + 0.6)
            
            # Create star shape with color variation
            if self.pulsating:
                star_color = QColor(255, 200 + int(55 * brightness), 255, int(255 * brightness))
            else:
                star_color = QColor(255, 255, 255, int(200 * brightness))
            
            painter.setBrush(QBrush(star_color))
            
            # Draw enhanced star
            star_size = sparkle['size'] * (0.5 + brightness * 0.5)
            self.draw_enhanced_star(painter, QPoint(int(x), int(y)), star_size, brightness)
    
    def draw_enhanced_star(self, painter, center, size, brightness):
        """Draw an enhanced 6-pointed star"""
        # Create a bright center
        center_color = QColor(255, 255, 255, int(255 * brightness))
        painter.setBrush(QBrush(center_color))
        painter.drawEllipse(center, int(size * 0.3), int(size * 0.3))
        
        # Draw star rays with gradient
        pen_color = QColor(center_color)
        pen_color.setAlpha(int(200 * brightness))
        pen = QPen(pen_color, max(1, int(size * 0.15)))
        painter.setPen(pen)
        
        # 6 rays at different angles
        for i in range(6):
            angle = i * (math.pi / 3)
            end_x = center.x() + size * math.cos(angle)
            end_y = center.y() + size * math.sin(angle)
            painter.drawLine(center, QPoint(int(end_x), int(end_y)))
    
    def draw_spectra_text(self, painter):
        """Draw the Spectra text with enhanced JARVIS-style effects"""
        # Set up font
        font = QFont("Segoe UI", 18, QFont.Bold)
        painter.setFont(font)
        
        # Calculate text position
        text = "SPECTRA"
        font_metrics = painter.fontMetrics()
        text_width = font_metrics.width(text)
        text_height = font_metrics.height()
        
        text_rect = QRectF(
            self.center.x() - text_width / 2,
            self.center.y() - text_height / 2 + 3,
            text_width,
            text_height
        )
        
        # Create multiple text glow layers
        glow_colors = [
            QColor(255, 255, 255, 40),
            QColor(self.color.red(), self.color.green(), self.color.blue(), 60)
        ]
        
        for i, glow_color in enumerate(glow_colors):
            painter.setPen(QPen(glow_color, 3 - i))
            painter.drawText(text_rect, Qt.AlignCenter, text)
        
        # Create advanced gradient for text
        text_gradient = QLinearGradient(text_rect.topLeft(), text_rect.bottomRight())
        if self.pulsating:
            # Dynamic rainbow gradient when listening
            phase = self.animation_phase
            r = int(255 * (math.sin(phase) * 0.3 + 0.7))
            g = int(255 * (math.sin(phase + 2.09) * 0.3 + 0.7))  # 120° offset
            b = int(255 * (math.sin(phase + 4.18) * 0.3 + 0.7))  # 240° offset
            
            text_gradient.setColorAt(0, QColor(r, g, b))
            text_gradient.setColorAt(0.5, QColor(255, 255, 255))
            text_gradient.setColorAt(1, QColor(b, r, g))
        else:
            # Elegant blue-white gradient
            text_gradient.setColorAt(0, QColor(180, 220, 255))
            text_gradient.setColorAt(0.3, QColor(255, 255, 255))
            text_gradient.setColorAt(0.7, QColor(255, 255, 255))
            text_gradient.setColorAt(1, QColor(200, 230, 255))
        
        painter.setPen(QPen(QBrush(text_gradient), 1))
        painter.drawText(text_rect, Qt.AlignCenter, text)
        
        # Add scanning line effect when active
        if self.pulsating:
            scan_y = text_rect.top() + (text_rect.height() * (self.animation_phase / (2 * math.pi)))
            scan_color = QColor(255, 255, 255, 150)
            scan_pen = QPen(scan_color, 1)
            painter.setPen(scan_pen)
            painter.drawLine(
                int(text_rect.left() - 10), int(scan_y),
                int(text_rect.right() + 10), int(scan_y)
            )
    
    def draw_status_indicator(self, painter):
        """Draw AI status indicator"""
        # Position at bottom of orb
        indicator_center = QPoint(self.center.x(), self.center.y() + 80)
        indicator_size = 6
        
        if self.pulsating:
            # Pulsing green dot when listening
            pulse_size = indicator_size * (1 + 0.5 * math.sin(self.animation_phase * 3))
            status_color = QColor(0, 255, 100, 200)
        else:
            # Static blue dot when idle
            pulse_size = indicator_size
            status_color = QColor(100, 150, 255, 150)
        
        # Draw indicator with glow
        glow_gradient = QRadialGradient(indicator_center, pulse_size * 2)
        glow_color = QColor(status_color)
        glow_color.setAlpha(50)
        glow_gradient.setColorAt(0, glow_color)
        glow_color.setAlpha(0)
        glow_gradient.setColorAt(1, glow_color)
        
        painter.setBrush(QBrush(glow_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(indicator_center, int(pulse_size * 2), int(pulse_size * 2))
        
        painter.setBrush(QBrush(status_color))
        painter.drawEllipse(indicator_center, int(pulse_size), int(pulse_size))
    
    def set_listening_state(self, listening):
        """Change orb appearance based on state"""
        self.pulsating = listening
        if listening:
            self.color = QColor(0, 200, 100)  # Green when listening
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
    
    def mouseDoubleClickEvent(self, event):
        """Double-click to toggle listening state"""
        if event.button() == Qt.LeftButton:
            self.set_listening_state(not self.pulsating)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    orb = AnimatedOrb()
    orb.show()
    
    # Demo: Toggle listening state every 4 seconds
    toggle_timer = QTimer()
    listening = False
    def toggle_state():
        global listening
        listening = not listening
        orb.set_listening_state(listening)
        print(f"AI State: {'LISTENING' if listening else 'IDLE'}")
    
    toggle_timer.timeout.connect(toggle_state)
    toggle_timer.start(4000)
    
    sys.exit(app.exec_())