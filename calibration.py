import speech_recognition as sr
import json
import argparse

def calibrate_noise_level(config_path='config.json', calibration_duration=5):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print(f"Calibrating for ambient noise. Please stay quiet during this time ({calibration_duration} seconds)...")
        recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
        noise_level = recognizer.energy_threshold
        print(f"Calibrated noise level: {noise_level}")

    # Load the existing configuration
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Update the noise level in the configuration
    config['recognition_settings']['noise_level'] = noise_level

    # Save the updated configuration
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

    print(f"Noise level has been updated in the configuration file: {config_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrate the noise level for the speech recognizer.")
    parser.add_argument("-c", "--config", type=str, default="config.json", help="Path to the configuration file.")
    parser.add_argument("-d", "--duration", type=int, default=5, help="Duration of the noise calibration in seconds.")
    args = parser.parse_args()

    calibrate_noise_level(config_path=args.config, calibration_duration=args.duration)