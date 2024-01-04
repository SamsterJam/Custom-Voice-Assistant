import pyaudio
import wave
import threading

def play_audio(audio_path):
    def play_stream():
        try:
            # Initialize PyAudio
            pa = pyaudio.PyAudio()

            # Open the sound file
            wf = wave.open(audio_path, 'rb')

            # Open a stream to play the sound
            stream = pa.open(
                format=pa.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            # Read data in chunks and play the sound
            data = wf.readframes(1024)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(1024)

        except Exception as e:
            print(f"An error occurred during playback: {e}")

        finally:
            # Close the stream and PyAudio
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            if 'pa' in locals():
                pa.terminate()

            # Close the wave file
            if 'wf' in locals():
                wf.close()

    # Create and start a new thread for the play_stream function
    thread = threading.Thread(target=play_stream)
    thread.start()