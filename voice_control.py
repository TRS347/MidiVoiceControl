import speech_recognition as sr
from threading import Thread

class VoiceControl:
    def __init__(self, midi_controller):
        self.recognizer = sr.Recognizer()
        self.midi_controller = midi_controller
        self.listening = True

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
        # Kanal auswählen
        channel_mapping = {
            "1": 1,
            "eins": 1,
            "2": 2,
            "zwei": 2,
            "3": 3,
            "drei": 3,
            "4": 4,
            "vier": 4

        }         
        # Notenwert-Mapping
        note_value_mapping = {
            "viertel": "viertel",
            "achtel": "achtel",
            "Achtel": "achtel",
            "sechzehntel": "sechzehntel",
            "16": "sechzehntel"  # Akzeptiere auch "16" als Befehl für Sechzehntel-Noten
        }
    
        if command.lower() in channel_mapping:
            channel = channel_mapping[command.lower()]
            self.midi_controller.set_channel(channel)
            print(f"Kanal {channel} wurde per Sprachbefehl ausgewählt.")
        
        # Start/Stop Befehl für den aktuellen Kanal
        elif "start" in command.lower() and self.midi_controller.selected_channel is not None:
            self.midi_controller.start_loop(self.midi_controller.selected_channel)
        
        elif "stop" in command.lower() and self.midi_controller.selected_channel is not None:
            self.midi_controller.stop_loop(self.midi_controller.selected_channel)
        
        elif command in note_value_mapping:
                note_value = note_value_mapping[command]
                if self.midi_controller.selected_channel is not None:
                    self.midi_controller.set_note_value(self.midi_controller.selected_channel, note_value)
                    print(f"Notenwert für Kanal {self.midi_controller.selected_channel} auf {note_value} gesetzt.")
                else:
                    print("Kein Kanal ausgewählt. Bitte zuerst einen Kanal auswählen.")

    def start(self):
        self.thread = Thread(target=self.listen_for_commands)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.listening = False
        if self.thread.is_alive():
            self.thread.join()
