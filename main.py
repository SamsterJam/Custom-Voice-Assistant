from wake_word_detector import WakeWordDetector
from audio_player import play_audio, play_voice
from speech_recognizer import SpeechRecognizer, Listen
from local_commands import process_for_local_command, ShutdownRequested
from openai_client import OpenAIClient
from voice_synthesis import VoiceSynthesizer
import json
import os
import time

# Load configuration from a JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Initializations
openai_client = OpenAIClient(config)
detector = WakeWordDetector()
recognizer = SpeechRecognizer()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['api-keys']['google_credentials']
voice_synthesizer = VoiceSynthesizer(config)

print("Listening for wake word...")

try:
    while True:
        if detector.wake_word_detected():
            print("Wake word detected!")
            play_audio('sounds/Wake.wav')
            
            status, command = recognizer.listen_for_speech()

            if status == Listen.SUCCESS:

                # Process local command

                # Check if the command is a local command
                if process_for_local_command(command):
                    continue  # Skip further processing if it's a local command

                play_audio('sounds/Heard.wav')
                print(f"Processing command: {command}")
                response = openai_client.process_with_gpt(command)
                play_audio('sounds/Received.wav')
                print(f"Assistant response: {response}")
                
                # Synthesize the response to speech
                audio_content = voice_synthesizer.synthesize_speech(response)
                if audio_content:
                    play_voice(audio_content)

            # No command heard
            elif status == Listen.NO_SPEECH:
                play_audio('sounds/NoSpeech.wav')

            # Error in transcribing command
            elif status == Listen.ERROR:
                play_audio('sounds/Error.wav')

except (KeyboardInterrupt, ShutdownRequested):
    print("Stopping...")

finally:
    # Perform any necessary cleanup before exiting
    openai_client.cleanup()
    detector.cleanup()
    recognizer.cleanup()
    voice_synthesizer.cleanup()