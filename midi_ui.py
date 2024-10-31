# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# class MidiUI(QWidget):
#     def __init__(self, midi_controller):
#         super().__init__()
#         self.midi_controller = midi_controller
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()
#         for channel in range(1, 5):
#             btn = QPushButton(f'Kanal {channel} abspielen')
#             btn.clicked.connect(lambda _, ch=channel: self.midi_controller.play_4_4_pattern(channel=ch, note=60))
#             layout.addWidget(btn)
#         self.setLayout(layout)
#         self.setWindowTitle('MIDI Controller')
#         self.show()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from midi_controller import MidiController

class MidiUI(QWidget):
    def __init__(self, midi_controller):
        super().__init__()
        self.midi_controller = midi_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Button für jeden der 4 Kanäle
        for channel in range(1, 5):
            btn = QPushButton(f'Kanal {channel} abspielen')
            btn.clicked.connect(lambda _, ch=channel: self.midi_controller.play_4_4_pattern(channel=ch, note=60))
            layout.addWidget(btn)

        # Button für das dauerhafte 4/4-Muster
        self.loop_button = QPushButton('Dauerhaftes 4/4-Muster starten')
        self.loop_button.clicked.connect(self.toggle_loop)
        layout.addWidget(self.loop_button)

        self.setLayout(layout)
        self.setWindowTitle('MIDI Controller')
        self.show()

    def toggle_loop(self):
        if self.midi_controller.looping:
            # Stoppen, wenn der Loop läuft
            self.midi_controller.stop_4_4_loop()
            self.loop_button.setText('Dauerhaftes 4/4-Muster starten')
        else:
            # Starten, wenn der Loop nicht läuft
            self.midi_controller.start_4_4_loop(channel=1, note=60, velocity=64)
            self.loop_button.setText('4/4-Muster stoppen')