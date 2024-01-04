from google.cloud import texttospeech
import os

class VoiceSynthesizer:
    def __init__(self, config):
        self.client = texttospeech.TextToSpeechClient()
        self.voice_settings = config['voice_settings']
        self.google_credentials = config['api-keys']['google_credentials']
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['api-keys']['google_credentials']

    def synthesize_speech(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=self.voice_settings['voice_name']
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            pitch=self.voice_settings['pitch'],
            speaking_rate=self.voice_settings['speaking_rate']
        )

        try:
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            print("Speech synthesized successfully")
            return response.audio_content
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return None

    def cleanup(self):
        # Perform any necessary cleanup
        pass