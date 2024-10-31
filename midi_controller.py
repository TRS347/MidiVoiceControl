import mido
import threading
import time

class MidiController:
    def __init__(self, port_name, bpm=120):
        self.port = mido.open_output(port_name)
        self.bpm = bpm
        self.beat_duration = 60 / bpm  # Grunddauer für einen Beat
        self.channels = {1: False, 2: False, 3: False, 4: False}  # Loop-Status je Kanal
        self.loop_threads = {}  # Aktive Threads für Loops
        self.note_values = {1: "viertel", 2: "viertel", 3: "viertel", 4: "viertel"}  # Standard-Notenwerte
        self.selected_channel = None  # Standard-Kanal, falls "Stopp" ohne Kanalangabe kommt
        self.start_event = threading.Event()  # Synchronisations-Event

    def set_channel(self, channel):
        self.selected_channel = channel
        print(f"Kanal {channel} ausgewählt.")

    def set_note_value(self, channel, note_value):
        self.note_values[channel] = note_value
        print(f"Notenwert für Kanal {channel} auf {note_value} gesetzt.")

    def start_loop(self, channel):
        if self.channels[channel]:
            print(f"Loop für Kanal {channel} läuft bereits.")
            return
        self.channels[channel] = True
        self.selected_channel = channel  # Setzt den Kanal als aktuellen
        self.loop_threads[channel] = threading.Thread(target=self._run_loop, args=(channel,))
        self.loop_threads[channel].start()
        self.start_event.set()  # Startet alle Threads synchron
        print(f"Loop für Kanal {channel} gestartet.")

    def stop_loop(self, channel=None):
        if channel is None:
            channel = self.selected_channel  # Verwende den zuletzt ausgewählten Kanal
        if channel is None or not self.channels[channel]:
            print(f"Loop für Kanal {channel} läuft nicht.")
            return
        self.channels[channel] = False
        if channel in self.loop_threads:
            self.loop_threads[channel].join()
            del self.loop_threads[channel]
        print(f"Loop für Kanal {channel} gestoppt.")

    def _run_loop(self, channel):
        self.start_event.wait()  # Alle Threads warten, bis das Event ausgelöst wird
        next_time = time.time()  # Starte den genauen Zeitstempel

        while self.channels[channel]:
            # MIDI-Befehl senden, basierend auf dem Taktwert
            duration = self._get_duration_from_note_value(channel)
            self.send_midi_message(channel, note=60, velocity=64)  # Verwende hier eine feste Note
            next_time += duration
            time.sleep(max(0, next_time - time.time()))  # Genaues Timing basierend auf dem nächsten Takt

    def send_midi_message(self, channel, note, velocity):
        msg = mido.Message('note_on', channel=channel-1, note=note, velocity=velocity)
        self.port.send(msg)
        time.sleep(0.1)  # Kurze Pause für die Note-Off Nachricht
        msg = mido.Message('note_off', channel=channel-1, note=note, velocity=velocity)
        self.port.send(msg)

    def _get_duration_from_note_value(self, channel):
        # Bestimmt die Dauer basierend auf dem Notenwert
        note_value = self.note_values.get(channel, "viertel")  # Standard ist Viertel
        if note_value == "viertel":
            return self.beat_duration
        elif note_value == "achtel":
            return self.beat_duration / 2
        elif note_value == "sechzehntel":
            return self.beat_duration / 4
        else:
            print(f"Unbekannter Notenwert '{note_value}' für Kanal {channel}, verwende Standard-Viertel.")
            return self.beat_duration  # Fallback zu Viertel
