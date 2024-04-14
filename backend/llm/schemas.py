from pydantic import BaseModel

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

    def __str__(self):
        return f"{self.name}: \n {self.content}"

class CalendarEvent(BaseModel):
    name: str
    description: str
    time: str

    def __str__(self):
        return f"{self.name} at {self.time}"

class Meeting(CalendarEvent):
    attendees: list[str]
    transcript: str

    def __str__(self):
        return f"{self.name} at {self.time} with {', '.join(self.attendees)}"

class Space(BaseModel):
    space_name: str
    user_name: str = None
    description: str | None = None
    calendar_events: list[CalendarEvent] | None = None
    documents: list[Document] | None = None

    def __str__(self):
        events = "\n".join([event for event in self.calendar_events]) if self.calendar_events else "No calendar events"
        docs = "\n".join([doc for doc in self.documents]) if self.documents else "No documents"

        return f"""
        Space: {self.space_name}, 
        Description: {self.description}, 
        Calendar Events: {events}, 
        Documents: {docs}"""