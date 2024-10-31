

import mido
import time
import threading

class MidiController:
    def __init__(self, port_name, bpm=120):
        self.port = mido.open_output(port_name)
        self.beat_duration = 60 / bpm  # Dauer eines Beats in Sekunden
        self.looping = False
        self.loop_thread = None

    def send_midi_message(self, channel, note=72, velocity=64):
        msg = mido.Message('note_on', channel=channel - 1, note=note, velocity=velocity)
        self.port.send(msg)
        time.sleep(0.1)  # Kurze Notenlänge
        self.port.send(mido.Message('note_off', channel=channel - 1, note=note))
        print(f"MIDI-Nachricht gesendet: Kanal {channel}, Note {note}, Velocity {velocity}")

    def play_4_4_pattern(self, channel=1, note=72, velocity=64, measures=2):
        total_beats = 4 * measures
        for _ in range(total_beats):
            self.send_midi_message(channel, note, velocity)
            time.sleep(self.beat_duration)
        print("4/4-Muster für 2 Takte abgeschlossen.")

    def start_4_4_loop(self, channel=1, note=72, velocity=64):
        if self.looping:
            return  # Verhindern, dass ein neuer Loop gestartet wird, während einer bereits läuft

        self.looping = True
        self.loop_thread = threading.Thread(target=self._run_4_4_loop, args=(channel, note, velocity))
        self.loop_thread.start()

    def _run_4_4_loop(self, channel, note, velocity):
        while self.looping:
            self.play_4_4_pattern(channel, note, velocity, measures=1)

    def stop_4_4_loop(self):
        self.looping = False
        if self.loop_thread is not None:
            self.loop_thread.join()  # Warte auf das Ende des Threads

    def stop(self):
        self.port.close()

