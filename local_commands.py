from audio_player import play_audio

class ShutdownRequested(Exception):
    pass

def stop_audio():
    print("Stopping audio...")
    # Add logic to stop audio playback

def cancel_command():
    print("Cancelling command...")
    play_audio("sounds/LocalCommand.wav")
    # Add logic to cancel the current operation

def shutdown():
    print("Shutting down...")
    play_audio("sounds/Shutdown.wav")
    raise ShutdownRequested()

# Define your local commands mapping
commands = {
    "stop": stop_audio,
    "nevermind": cancel_command,
    "never mind": cancel_command,
    "cancel": cancel_command,
    "shutdown": shutdown,
    "shut down": shutdown,
}

def process_for_local_command(command):
    """Handle a local command if it exists, and return True if handled."""
    command_function = commands.get(command.lower())
    if command_function:
        command_function()
        return True
    return False