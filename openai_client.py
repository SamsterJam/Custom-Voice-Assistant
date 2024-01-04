class OpenAIClient:
    def __init__(self, config):
        self.config = config
    
    def process_with_gpt(self, command):
        return f"I understand you command is '{command}' and it has been dummy-processed by gpt"
    
    def cleanup(self):
        pass