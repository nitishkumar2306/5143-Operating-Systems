"""
Import the 'logging' module, which provides a flexible libraries for emitting log messages.
"""
import logging

class PrintCaptureLogger:
    def __init__(self):
        # Initialize an empty list to capture log messages

        self.log_content = []

    def write(self, message):
        # Append log messages to the 'log_content' list
        self.log_content.append(message)
    
     
