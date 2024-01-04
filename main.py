from wake_word_detector import WakeWordDetector
from audio_player import play_audio
from speech_recognizer import SpeechRecognizer, Listen
from openai_client import OpenAIClient
import json

# Load configuration from a JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Initialize the OpenAI client
openai_client = OpenAIClient(config)

# Initialize WakeWordDetector and SpeechRecognizer
detector = WakeWordDetector()
recognizer = SpeechRecognizer()

print("Listening for wake word...")

try:
    while True:
        if detector.wake_word_detected():
            print("Wake word detected!")
            play_audio('sounds/Wake.wav')
            
            status, command = recognizer.listen_for_speech()

            # Command was heard
            if status == Listen.SUCCESS:
                play_audio('sounds/Heard.wav')
                print(f"Processing command: {command}")
                response = openai_client.process_with_gpt(command)
                print(f"Assistant response: {response}")

            # No command heard
            elif status == Listen.NO_SPEECH:
                play_audio('sounds/NoSpeech.wav')

            # Error in transcribing command
            elif status == Listen.ERROR:
                play_audio('sounds/Error.wav')

except KeyboardInterrupt:
    print("Stopping...")

finally:
    # Perform any necessary cleanup before exiting
    openai_client.cleanup()
    detector.cleanup()
    recognizer.cleanup()