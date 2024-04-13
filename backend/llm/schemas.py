from pydantic import BaseModel, Field

"""
SCHEMAS FOR GENERATION TASKS 
"""
# Generating tasks
class Task(BaseModel):
    task: str
    description: str

class MeetingTasks(BaseModel):
    tasks: list[Task]

# Generating summary of meeting
class Point(BaseModel):
    point: str

class MeetingSummary(BaseModel):
    main_points: list[Point]

# Generating email drafts
class EmailDraft(BaseModel):
    recipient: str
    subject: str
    body: str

class EmailDrafts(BaseModel):
    drafts: list[EmailDraft]

"""
SCHEMAS FOR CONTEXT ABOUT SPACES 
"""
# if we build out the context about the space that the user is in, we can use that as context for the model
# idea: use the Google Workspace APIs, generate the classes modeling the spaces, and inject that into all the generation prompts so model is context aware

class Document(BaseModel):
    name: str
    content: str

class CalendarEvent(BaseModel):
    name: str
    description: str
    time: str

class Meeting(CalendarEvent):
    attendees: list[str]
    transcript: str

class Space(BaseModel):
    name: str
    description: str
    calendar_events: list[CalendarEvent] | None
    documents: list[Document] | None