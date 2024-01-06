import json
import pvporcupine
import pyaudio
import struct

class WakeWordDetector:
    def __init__(self, config_path='config.json'):
        # Load configuration from config.json
        with open(config_path) as config_file:
            config = json.load(config_file)

        # Get the API keys and other settings from the config file
        porcupine_access_key = config['api-keys']['porcupine_api_key']
        wake_word_path = config['wake_word_settings']['custom_wake_word_file']

        # Initialize Porcupine
        self.porcupine = pvporcupine.create(access_key=porcupine_access_key, keyword_paths=[wake_word_path])

        # Initialize PyAudio
        self.pa = pyaudio.PyAudio()

        # Open audio stream for Porcupine
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def wake_word_detected(self):
        pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
        keyword_index = self.porcupine.process(pcm)
        return keyword_index >= 0

    def cleanup(self):
        self.audio_stream.close()
        self.pa.terminate()
        self.porcupine.delete()