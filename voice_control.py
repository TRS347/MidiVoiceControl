import speech_recognition as sr
from threading import Thread

class VoiceControl:
    def __init__(self, midi_controller):
        self.recognizer = sr.Recognizer()
        self.midi_controller = midi_controller
        self.listening = True     
        self.selected_channel = None


    def listen_for_commands(self):
        while self.listening:
            try:
                with sr.Microphone() as source:
                    print("Sprich deinen Befehl...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)
                command = self.recognizer.recognize_google(audio, language="de-DE")
                print(f"Erkannter Befehl: {command}")
                self.process_command(command)
            except sr.WaitTimeoutError:
                print("Kein Ton erkannt. Versuche es erneut...")
            except sr.UnknownValueError:
                print("Befehl nicht verstanden")
            except sr.RequestError:
                print("Fehler beim Abrufen der Sprachdaten")

    def process_command(self, command):
        # Kanal- und Notenwert-Mappings
        channel_mapping = {
            "1": 1, "eins": 1, "kick": 1, "kik": 1, "kikk": 1,
            "2": 2, "zwei": 2, "snare": 2,
            "3": 3, "drei": 3, "hihat": 3, "hyatt": 3,
            "4": 4, "vier": 4
        }
        note_value_mapping = {
            "halbe": "halbe", "halb": "halbe",
            "viertel": "viertel", "vier": "viertel", "viertelnote": "viertel",
            "achtel": "achtel", "acht": "achtel", "achtelnote": "achtel",
            "sechzehntel": "sechzehntel", "sechzehn": "sechzehntel", "16": "sechzehntel"
        }

        # Zerlege den Befehl in einzelne Wörter
        words = command.lower().strip().split()
        print(f"Verarbeitete Wörter: {words}")  # Debugging-Output

        selected_channel = None
        action = None
        note_value = None
        all_channels_action = False

        # Prüfe jedes Wort im Befehl und speichere die erkannte Information
        for word in words:
            if word in channel_mapping:
                selected_channel = channel_mapping[word]  # Nur lokal setzen
                self.selected_channel = selected_channel  # Aktualisiere den gespeicherten Kanal
                print(f"Kanal {self.selected_channel} wurde per Sprachbefehl ausgewählt.")
            elif word == "start":
                action = "start"
            elif word == "stopp":
                action = "stop"
            elif word in note_value_mapping:
                note_value = note_value_mapping[word]
            elif word == "beat" and "start" in words:
                all_channels_action = "start"
            elif word == "beat" and "stop" in words:
                all_channels_action = "stop"

        # Nutze den zuletzt ausgewählten Kanal, wenn keiner im aktuellen Befehl angegeben wurde
        if selected_channel is None:
            selected_channel = self.selected_channel

        # Zusätzliche Debugging-Informationen
        if selected_channel is None:
            print("Kein Kanal ausgewählt.")
        if action is None:
            print("Keine gültige Aktion erkannt.")
        if not (selected_channel or action or note_value):
            print("Kein gültiger Befehl erkannt.")


        # Wenn "Beat Start" oder "Beat Stop" erkannt wurde
        if all_channels_action == "start":
            self.midi_controller.start_all_loops()
            print("Alle Kanäle wurden gestartet.")
        elif all_channels_action == "stop":
            self.midi_controller.stop_all_loops()
            print("Alle Kanäle wurden gestoppt.")

        # Aktionen basierend auf den erkannten Wörtern
        if action == "start" and selected_channel is not None:
            self.midi_controller.start_loop(selected_channel)
            print(f"Loop für Kanal {selected_channel} gestartet.")
        elif action == "stop" and selected_channel is not None:
            self.midi_controller.stop_loop(selected_channel)
            print(f"Loop für Kanal {selected_channel} gestoppt.")
        else:
            print("Aktion konnte nicht ausgeführt werden, Kanal oder Aktion fehlt.")

        # Setze den Notenwert, falls dieser erkannt wurde und ein Kanal ausgewählt ist
        if note_value and selected_channel is not None:
            self.midi_controller.set_note_value(selected_channel, note_value)
            print(f"Notenwert für Kanal {selected_channel} auf {note_value} gesetzt.")

        # Wenn keine der Aktionen erkannt wurde
        if not (selected_channel or action or note_value):
            print("Kein gültiger Befehl erkannt.")

    def start(self):
        self.thread = Thread(target=self.listen_for_commands)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.listening = False
        if self.thread.is_alive():
            self.thread.join()