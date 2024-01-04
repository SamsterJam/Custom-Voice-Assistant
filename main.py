from wake_word_detector import WakeWordDetector
from audio_player import play_audio
from speech_recognizer import SpeechRecognizer
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
            
            # Listen for speech after wake word is detected
            command = recognizer.listen_for_speech()
            if command:
                play_audio('sounds/Heard.wav')
                # Process the recognized speech command using the OpenAI client
                print(f"Processing command: {command}")
                response = openai_client.process_with_gpt(command)
                print(f"Assistant response: {response}")
                
                # Optionally, play a response or perform an action based on the assistant's response

except KeyboardInterrupt:
    print("Stopping...")

finally:
    # Perform any necessary cleanup before exiting
    openai_client.cleanup()
    detector.cleanup()
    recognizer.cleanup()