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

def generate_ics_content(meeting: dict, mail_sender: str) -> str:
    """
    Generates standard ICS calendar invite content.
    """
    import datetime
    dt_str = meeting.get("date_time", "")
    
    # Simple parse attempt, fallback if it is not custom formatted
    try:
        # Standard formats like "YYYY-MM-DD HH:MM" or ISO "YYYY-MM-DDTHH:MM:SS"
        import dateutil.parser
        dt_parsed = dateutil.parser.parse(dt_str)
    except Exception:
        try:
            dt_parsed = datetime.datetime.fromisoformat(dt_str)
        except Exception:
            dt_parsed = datetime.datetime.now()
            
    dt_start_str = dt_parsed.strftime("%Y%m%dT%H%M%SZ")
    duration = meeting.get("duration_minutes", 30)
    dt_end = dt_parsed + datetime.timedelta(minutes=duration)
    dt_end_str = dt_end.strftime("%Y%m%dT%H%M%SZ")
    
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Karan Systems//Meeting Scheduler//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:REQUEST",
        "BEGIN:VEVENT",
        f"UID:{meeting.get('id', 'uid')}@karansystem.com",
        f"DTSTAMP:{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART:{dt_start_str}",
        f"DTEND:{dt_end_str}",
        f"SUMMARY:{meeting.get('subject', 'Meeting Invite')}",
        f"DESCRIPTION:{meeting.get('agenda', '')}",
        f"ORGANIZER;CN=Karan Systems BOT:MAILTO:{mail_sender}",
    ]
    for p in meeting.get("participants", []):
        ics_lines.append(f"ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE:MAILTO:{p}")
    
    ics_lines.extend([
        "END:VEVENT",
        "END:VCALENDAR"
    ])
    return "\n".join(ics_lines)

if __name__ == "__main__":
    # Run the server via stdio transport
    mcp.run(transport="stdio")
