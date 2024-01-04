import speech_recognition as sr
import json
from enum import Enum, auto

# Listen Status
class Listen(Enum):
    SUCCESS = auto()
    NO_SPEECH = auto()
    ERROR = auto()


class SpeechRecognizer:
    def __init__(self, config_path='config.json'):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            rec_settings = config['recognition_settings']
            self.noise_level = rec_settings.get('noise_level', self.recognizer.energy_threshold)
            self.command_await_timeout = rec_settings['command_await_timeout']
            self.recognizer.pause_threshold = rec_settings['recognizer_pause_threshold']
            self.recognizer.phrase_threshold = rec_settings['recognizer_phrase_threshold']
            self.recognizer.non_speaking_duration = rec_settings['recognizer_non_speaking_duration']

    def listen_for_speech(self):
        # Use the calibrated noise level
        self.recognizer.energy_threshold = self.noise_level
        #print(f"Using calibrated noise level: {self.noise_level}")

        with self.microphone as source:
            print("Listening for speech...")
            try:
                audio = self.recognizer.listen(source, timeout=self.command_await_timeout)
            except sr.WaitTimeoutError:
                print(f"No speech detected within {self.command_await_timeout} seconds.")
                return Listen.NO_SPEECH, None

        try:
            text = self.recognizer.recognize_google(audio)
            return Listen.SUCCESS, text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
            return Listen.NO_SPEECH, None
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return Listen.ERROR, None

    def cleanup(self):
        # Perform any necessary cleanup actions
        pass