import sys
from PyQt5.QtWidgets import QApplication
from midi_controller import MidiController
from voice_control import VoiceControl
from midi_ui import MidiUI

# MIDI-Controller initialisieren
midi_controller = MidiController('IAC-Treiber Bus 1')  # Ersetze durch deinen MIDI-Port-Namen

# Initialisiere die Sprachsteuerung
voice_control = VoiceControl(midi_controller)
voice_control.start()


# GUI starten
app = QApplication(sys.argv)
midi_ui = MidiUI(midi_controller)

# Sprachsteuerung starten (optional in einem separaten Thread)
# voice_control.listen_for_commands()

sys.exit(app.exec_())

