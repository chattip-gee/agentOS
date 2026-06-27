# tools/drive_tool.py
# AgentOS - Google Drive MCP Tool
# Saves agent reports to Google Drive automatically

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# Google Drive API scope - read and write access
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

class DriveTool:
    """
    MCP Google Drive Tool
    Enables AgentOS to save reports directly to Google Drive.
    This is the MCP (Model Context Protocol) integration layer.
    """

    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        """
        Authenticate with Google Drive API using OAuth 2.0.
        First run will open browser for user consent.
        Subsequent runs use saved token.json.
        """
        creds = None

        # Load existing token if available
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json", SCOPES
            )

        # If no valid credentials, request new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save token for future runs
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    def save_report(self, filename: str, content: str, task_id: str):
        """
        Save a report to Google Drive as a text file.
        filename: name of the file in Google Drive
        content: text content to save
        task_id: task ID for tracking
        """
        print(f"\n☁️ MCP Drive Tool: Saving report to Google Drive...")

        # Convert content to bytes for upload
        file_content = content.encode("utf-8")
        media = MediaInMemoryUpload(
            file_content,
            mimetype="text/plain",
            resumable=False
        )

        # File metadata
        file_metadata = {
            "name": f"{filename}_{task_id}.txt",
            "description": f"AgentOS Report - Task {task_id}"
        }

        # Upload to Google Drive
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink"
        ).execute()

        print(f"✅ Report saved to Google Drive!")
        print(f"📁 File: {file.get('name')}")
        print(f"🔗 Link: {file.get('webViewLink')}")

        return file.get("webViewLink")