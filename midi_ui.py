from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
from midi_controller import MidiController

class MidiUI(QWidget):
    def __init__(self, midi_controller):
        super().__init__()
        self.midi_controller = midi_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Kanal-Auswahl mit Buttons für jeden der 4 Kanäle
        channel_label = QLabel("Kanal auswählen:")
        layout.addWidget(channel_label)
        
        for channel in range(1, 5):
            btn = QPushButton(f"Kanal {channel} auswählen")
            btn.clicked.connect(lambda _, ch=channel: self.select_channel(ch))
            layout.addWidget(btn)

        # Notenwert-Auswahl
        note_label = QLabel("Notenwert auswählen:")
        layout.addWidget(note_label)

        self.note_value_combo = QComboBox()
        self.note_value_combo.addItems(["Viertel", "Achtel", "Sechzehntel"])
        self.note_value_combo.currentTextChanged.connect(self.change_note_value)
        layout.addWidget(self.note_value_combo)

        # Button für den aktuellen Kanal-Loop starten/stoppen
        self.loop_button = QPushButton("Loop starten")
        self.loop_button.clicked.connect(self.toggle_loop)
        layout.addWidget(self.loop_button)

        self.setLayout(layout)
        self.setWindowTitle('MIDI Controller')
        self.show()

    def select_channel(self, channel):
        """Wählt den Kanal aus und zeigt eine Rückmeldung."""
        self.midi_controller.set_channel(channel)
        print(f"Kanal {channel} wurde ausgewählt.")

    def change_note_value(self, note_value):
        """Ändert den Notenwert des ausgewählten Kanals."""
        if self.midi_controller.selected_channel is not None:
            # Mapped `note_value` text to controller-compatible string
            note_value_map = {
                "Viertel": "viertel",
                "Achtel": "achtel",
                "Sechzehntel": "sechzehntel"
            }
            self.midi_controller.set_note_value(self.midi_controller.selected_channel, note_value_map[note_value])
            print(f"Notenwert für Kanal {self.midi_controller.selected_channel} auf {note_value_map[note_value]} gesetzt.")
        else:
            print("Kein Kanal ausgewählt. Bitte zuerst einen Kanal auswählen.")

    def toggle_loop(self):
        """Startet oder stoppt den Loop für den ausgewählten Kanal."""
        if self.midi_controller.selected_channel is None:
            print("Kein Kanal ausgewählt. Bitte zuerst einen Kanal auswählen.")
            return

        if self.midi_controller.selected_channel in self.midi_controller.channel_loops:
            # Loop läuft bereits, daher stoppen
            self.midi_controller.stop_loop(self.midi_controller.selected_channel)
            self.loop_button.setText("Loop starten")
            print(f"Loop für Kanal {self.midi_controller.selected_channel} gestoppt.")
        else:
            # Loop starten
            self.midi_controller.start_loop(self.midi_controller.selected_channel)
            self.loop_button.setText("Loop stoppen")
            print(f"Loop für Kanal {self.midi_controller.selected_channel} gestartet.")
