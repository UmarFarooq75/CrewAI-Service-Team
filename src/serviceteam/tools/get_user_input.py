from crewai_tools import tool
from datetime import datetime

class GetUserInput:
    @staticmethod
    @tool("get_input_for_meeting")
    def get_input_for_meeting() -> dict:
        """Use this tool to get user input for scheduling a meeting."""
        description = input("Please enter the description for the meeting: ")
        start_time = GetUserInput.get_valid_datetime_input("Please enter the start time for the meeting (YYYY-MM-DDTHH:MM:SSZ): ")
        end_time = GetUserInput.get_valid_datetime_input("Please enter the end time for the meeting (YYYY-MM-DDTHH:MM:SSZ): ")
        attendee_email = input("Please enter the attendee's email address: ")
        summary = input("Please enter a summary for the meeting: ")
        
        meeting_data = {
            "description": description,
            "start_time": start_time,
            "end_time": end_time,
            "attendee_email": attendee_email,
            "summary": summary
        }
        return meeting_data

    @staticmethod
    def get_valid_datetime_input(prompt: str) -> str:
        """Prompt user for a valid datetime input."""
        while True:
            datetime_input = input(prompt)
            try:
                datetime.strptime(datetime_input, "%Y-%m-%dT%H:%M:%SZ")
                return datetime_input
            except ValueError:
                print("Invalid datetime format. Please enter in the format YYYY-MM-DDTHH:MM:SSZ.")
