import mido
import time
import threading

class MidiController:
    def __init__(self, port_name, bpm=120):
        self.port = mido.open_output(port_name)
        self.beat_duration = 60 / bpm  # Dauer eines Beats in Sekunden
        self.channel_loops = {}  # Verwaltung der aktiven Loops
        self.selected_channel = None  # Aktuell ausgewählter Kanal
        self.note_values = {  # Notenwerte für jeden Kanal
            1: "viertel",
            2: "viertel",
            3: "viertel",
            4: "viertel"
        }

    def set_channel(self, channel):
        self.selected_channel = channel
        print(f"Kanal {channel} ausgewählt.")

    def set_note_value(self, channel, note_value):
        self.note_values[channel] = note_value
        print(f"Notenwert für Kanal {channel} auf {note_value} gesetzt.")

    def get_beat_duration(self, note_value):
        if note_value == "viertel":
            return self.beat_duration
        elif note_value == "achtel":
            return self.beat_duration / 2
        elif note_value == "sechzehntel":
            return self.beat_duration / 4
        return self.beat_duration

    def play_pattern(self, channel, note=72, velocity=64):
        note_value = self.note_values[channel]
        duration = self.get_beat_duration(note_value)
        msg = mido.Message('note_on', channel=channel - 1, note=note, velocity=velocity)
        self.port.send(msg)
        time.sleep(0.1)  # Kurze Notenlänge
        self.port.send(mido.Message('note_off', channel=channel - 1, note=note))
        time.sleep(duration - 0.1)  # Pause basierend auf Notenwert

    def start_loop(self, channel):
        if channel in self.channel_loops and self.channel_loops[channel]["looping"]:
            return  # Der Loop läuft bereits für diesen Kanal

        self.channel_loops[channel] = {
            "looping": True,
            "thread": threading.Thread(target=self._run_loop, args=(channel,))
        }
        self.channel_loops[channel]["thread"].start()
        print(f"Loop für Kanal {channel} gestartet.")

    def _run_loop(self, channel):
        while self.channel_loops[channel]["looping"]:
            self.play_pattern(channel)

    def stop_loop(self, channel):
        if channel in self.channel_loops and self.channel_loops[channel]["looping"]:
            self.channel_loops[channel]["looping"] = False
            self.channel_loops[channel]["thread"].join()
            del self.channel_loops[channel]
            print(f"Loop für Kanal {channel} gestoppt.")
