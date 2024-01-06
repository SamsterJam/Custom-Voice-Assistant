import openai
from pathlib import Path
import json
import importlib
from audio_player import play_audio
import datetime

class OpenAIClient:
    def __init__(self, config):
        self.config = config
        self.client = openai.OpenAI(api_key=config['api-keys']['openai_api_key'])
        self.model = config["assistant-settings"]["model"]
        self.assistant_id = None
        self.thread_id = None
        self.active_threads_file = Path('.active-threads')
        self.active_assistants_file = Path('.active-assistants')
        self.load_active_resources()
        self.create_assistant_and_thread()

    def load_active_resources(self):
        # Close and clean up any orphaned assistants or threads
        if self.active_assistants_file.exists():
            with open(self.active_assistants_file, 'r') as file:
                for line in file:
                    assistant_id = line.strip()
                    self.close_assistant(assistant_id)
            self.active_assistants_file.unlink()

        if self.active_threads_file.exists():
            with open(self.active_threads_file, 'r') as file:
                for line in file:
                    thread_id = line.strip()
                    self.close_thread(thread_id)
            self.active_threads_file.unlink()

    def create_assistant_and_thread(self):
        # Load prompt and tools from files
        try:
            with open('assistant-prompt.txt', 'r') as file:
                instructions = file.read()
                instructions += f"\n IMPORTANT: Check the date before retreiving the weather, as of now it is {datetime.datetime}"
        except FileNotFoundError:
            print("The file 'assistant-prompt.txt' does not exist. Please move or rename 'assistant-prompt-template.txt' to 'assistant-prompt.txt'.")
        
        with open('assistant-tools.json', 'r') as file:
            tools = json.load(file)

        # Create an Assistant
        assistant_response = self.client.beta.assistants.create(
            name="Voice-Assistant",
            instructions=instructions,
            tools=tools,
            model=self.model
        )
        self.assistant_id = assistant_response.id
        with open(self.active_assistants_file, 'w') as file:
            file.write(self.assistant_id + '\n')

        # Create a Thread
        thread_response = self.client.beta.threads.create()
        self.thread_id = thread_response.id
        with open(self.active_threads_file, 'w') as file:
            file.write(self.thread_id + '\n')

    def process_with_gpt(self, command):
        # Add a Message to the Thread
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=command
        )

        # Run the Assistant
        run_response = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )
        run_id = run_response.id

        # Check the Run status and wait for completion
        run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run_id  # Use the variable instead of subscript notation
        )
        while run.status != 'completed':
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run_id  # Use the variable instead of subscript notation
            )
            # Check if the run requires action (function calling)
            if run.status == 'requires_action':
                self.handle_required_action(run)

        # Retrieve the Assistant's response
        messages_response = self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        # Sort the messages by creation time and filter for assistant messages
        assistant_messages = sorted(
            (msg for msg in messages_response.data if msg.role == 'assistant'),
            key=lambda m: m.created_at
        )
        # Get the latest assistant message
        latest_assistant_message = assistant_messages[-1].content[0].text.value if assistant_messages else "No response."
        return latest_assistant_message

    def handle_required_action(self, run):
        # Retrieve the required actions from the run
        required_actions = run.required_action.submit_tool_outputs.tool_calls

        # Initialize the list to store tool outputs
        tool_outputs = []

        # Process each required action
        for action in required_actions:
            function_name = action.function.name
            arguments = json.loads(action.function.arguments)

            print(f"Assistant called: '{function_name}({arguments})'")
            # Import the module from the 'assistant-modules' folder
            module = importlib.import_module(f'assistant-modules.{function_name}')
            function = getattr(module, function_name)

            # Call the function with the provided arguments
            play_audio('sounds/Request.wav')
            output = function(**arguments)

            # Append the output to the tool_outputs list
            tool_outputs.append({
                "tool_call_id": action.id,  
                "output": output,
            })

            play_audio('sounds/Received.wav')
            print(f"Assistant received: '{output}'")

        # Submit all the tool outputs together to continue the run
        if tool_outputs:
            self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )


    def close_assistant(self, assistant_id):
        try:
            print(f"Closing assistant with ID: {assistant_id}")
            self.client.beta.assistants.delete(assistant_id)
        except Exception as e:
            print(f"Failed to close assistant with ID {assistant_id}: {e}")

    def close_thread(self, thread_id):
        try:
            print(f"Closing thread with ID: {thread_id}")
            self.client.beta.threads.delete(thread_id)
        except Exception as e:
            print(f"Failed to close thread with ID {thread_id}: {e}")

    def cleanup(self):
        # Perform cleanup, such as closing the assistant and thread
        if self.assistant_id:
            self.close_assistant(self.assistant_id)
        if self.thread_id:
            self.close_thread(self.thread_id)
        if self.active_assistants_file.exists():
            self.active_assistants_file.unlink()
        if self.active_threads_file.exists():
            self.active_threads_file.unlink()