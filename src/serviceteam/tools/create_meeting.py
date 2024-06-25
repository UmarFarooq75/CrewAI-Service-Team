import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from crewai_tools import tool

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class CreateMeeting:
    # @staticmethod
    # @tool("create_meeting")
    # def call_create_meeting(tool_input:dict) -> str:
    #     """Use this tool to create meeting in our calendar with customers this tool requires input from user his email , name date and description"""
    #     return CreateMeeting.create_meeting(
    #         tool_input["description"],
    #         tool_input["start_time"],
    #         tool_input["end_time"],
    #         tool_input["attendee_email"],
    #         tool_input["summary"]
    #     )   
    @staticmethod
    @tool("create_meeting")
    def create_meeting(description: str, start_time: str, end_time: str, attendee_email: str, summary: str) -> str:
        """Create a meeting on Google Calendar."""
        file_path = "E:/GenAI/serviceteam/src/serviceteam/tools/token.json"
        file_path1="E:/GenAI/serviceteam/src/serviceteam/tools/credentials.json"
        if not os.path.exists(file_path):
            return f"Error: The file at {file_path} does not exist."
        if not os.path.exists(file_path):
            return f"Error: The file at {file_path1} does not exist."
        
        
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(file_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(file_path1, SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        
        try:
            service = build("calendar", "v3", credentials=creds)
            event = {
                'summary': summary,
                "colorId": 5,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC',
                },
                'attendees': [{'email': attendee_email}],
                'reminders': {
                    'useDefault': True,
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            return event.get('htmlLink')
        except HttpError as error:
            return f"An error occurred: {error}"

# Example usage
# if __name__ == "__main__":
#     tool_input = {
#         "description": "Project discussion",
#         "start_time": "2024-06-11T04:22:00Z",
#         "end_time": "2024-06-11T08:22:00Z",
#         "attendee_email": "attendee@example.com",
#         "summary": "Meeting Summary"
#     }
    
#     tool = CreateMeeting.call_create_meeting(tool_input)
#     print(tool)
