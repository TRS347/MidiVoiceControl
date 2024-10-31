

# import speech_recognition as sr
# from threading import Thread

# class VoiceControl:
#     def __init__(self, midi_controller):
#         self.recognizer = sr.Recognizer()
#         self.recognizer.energy_threshold = 300  # Empfindlichkeit für Hintergrundgeräusche
#         self.recognizer.pause_threshold = 0.5  # Kürzere Pausen als Ende des Sprechens erkennen

#         self.midi_controller = midi_controller
#         self.listening = True

#     def listen_for_commands(self):
#         while self.listening:
#             try:
#                 with sr.Microphone() as source:
#                     print("Sprich deinen Befehl...")
#                     self.recognizer.energy_threshold = 300
#                     self.recognizer.pause_threshold = 0.5
#                     audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
#                 command = self.recognizer.recognize_google(audio, language="de-DE")
#                 print(f"Erkannter Befehl: {command}")
#                 self.process_command(command)
#             except sr.WaitTimeoutError:
#                 print("Kein Ton erkannt. Versuche es erneut...")
#             except sr.UnknownValueError:
#                 print("Befehl nicht verstanden")
#             except sr.RequestError:
#                 print("Fehler beim Abrufen der Sprachdaten")

#     def process_command(self, command):
#         if "start" in command.lower():
#             if not self.midi_controller.looping:
#                 print("Start des 4/4-Takt Loops")
#                 self.midi_controller.start_4_4_loop(channel=1, note=60, velocity=64)
#         elif "stop" in command.lower():
#             if self.midi_controller.looping:
#                 print("Stopp des 4/4-Takt Loops")
#                 self.midi_controller.stop_4_4_loop()
    
#     def start(self):
#         # Starte die Sprachsteuerung in einem separaten Thread
#         self.thread = Thread(target=self.listen_for_commands)
#         self.thread.daemon = True
#         self.thread.start()
    
#     def stop(self):
#         self.listening = False
#         if self.thread.is_alive():
#             self.thread.join()

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
        if "start" in command.lower():
            if not self.midi_controller.looping:
                print("Start des 4/4-Takt Loops")
                self.midi_controller.start_4_4_loop(channel=1, note=60, velocity=64)
        elif "stopp" in command.lower():
            if self.midi_controller.looping:
                print("Stopp des 4/4-Takt Loops")
                self.midi_controller.stop_4_4_loop()


    def start(self):
        self.thread = Thread(target=self.listen_for_commands)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.listening = False
        if self.thread.is_alive():
            self.thread.join()
