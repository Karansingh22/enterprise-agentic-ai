import sys
import os

# Ensure the project root is on sys.path so `config` can be imported
# when this file is run as a subprocess from the tools/ directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
from config import MAIL_SENDER, MAIL_PASSWORD, SMTP_HOST, SMTP_PORT
import json
import uuid
import os

# Initialize FastMCP server
mcp = FastMCP("MeetingScheduler")

DRAFTS_FILE = os.path.join(os.path.dirname(__file__), "drafts.json")

def load_drafts():
    if os.path.exists(DRAFTS_FILE):
        with open(DRAFTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_drafts(drafts):
    with open(DRAFTS_FILE, "w") as f:
        json.dump(drafts, f, indent=4)

class MeetingDraft(BaseModel):
    id: str
    subject: str
    participants: list[str]
    date_time: str
    duration_minutes: int
    agenda: str
    status: str

@mcp.tool()
def draft_meeting(
    subject: str,
    participants: list[str],
    date_time: str,
    duration_minutes: int,
    agenda: str
) -> str:
    """
    Drafts a meeting email to be reviewed by the user before sending.
    Always call this FIRST when a user asks to schedule a meeting.
    Returns the JSON representation of the drafted meeting along with its draft ID.
    """
    draft_id = str(uuid.uuid4())[:8]
    
    draft = {
        "id": draft_id,
        "subject": subject,
        "participants": participants,
        "date_time": date_time,
        "duration_minutes": duration_minutes,
        "agenda": agenda,
        "status": "drafted_pending_approval"
    }
    
    drafts = load_drafts()
    drafts[draft_id] = draft
    save_drafts(drafts)
    
    response_msg = (
        f"Meeting drafted successfully!\n\n"
        f"Draft ID: {draft_id}\n"
        f"Subject: {subject}\n"
        f"To: {', '.join(participants)}\n"
        f"When: {date_time} (Duration: {duration_minutes} mins)\n"
        f"Agenda: {agenda}\n\n"
        f"To finalize and send this meeting invite, use the send_meeting_email tool with Draft ID: {draft_id}."
    )
    return response_msg

@mcp.tool()
def send_meeting_email(draft_id: str) -> str:
    """
    Sends the email for a drafted meeting. ONLY call this AFTER the user has explicitly confirmed
    the drafted details and asked you to send it.
    """
    drafts = load_drafts()
    
    if draft_id not in drafts:
        return f"Error: Draft ID '{draft_id}' not found."
        
    draft = drafts[draft_id]
    
    # Check credentials
    if not MAIL_PASSWORD or MAIL_PASSWORD == "your_app_password_here":
        return "Error: SMTP credentials (MAIL_PASSWORD) are missing or not configured. Cannot send email."

    msg = MIMEMultipart()
    msg['From'] = MAIL_SENDER
    msg['To'] = ", ".join(draft['participants'])
    msg['Subject'] = f"Meeting Invite: {draft['subject']}"
    
    body = f"""
    You have been invited to a meeting.
    
    Subject: {draft['subject']}
    Date & Time: {draft['date_time']}
    Duration: {draft['duration_minutes']} minutes
    
    Agenda:
    {draft['agenda']}
    
    Best regards,
    Karan Systems BOT
    """
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(MAIL_SENDER, MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        draft['status'] = "sent"
        save_drafts(drafts)
        return f"Success! Meeting email sent to {msg['To']} for draft {draft_id}."
    except Exception as e:
        return f"Failed to send email via SMTP. Error: {str(e)}"

if __name__ == "__main__":
    # Run the server via stdio transport
    mcp.run(transport="stdio")
