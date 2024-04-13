from wrappers.gemini_chat import GeminiClient
import prompts
from schemas import (
    MeetingTasks,
    MeetingSummary,
    EmailDrafts,
    Space
)

"""

Gemini wrapper associated with a Space.

If a Space is updated, a new Companion should be created.

The provided Space is used to generate context-aware prompts for the user.

"""
class Companion(GeminiClient):
    def __init__(self, space: Space, 
                       model: str = "gemini-1.5-pro-latest", 
                       api_key: str | None = None,  
                       debug: bool = False, 
                       system_message: str = prompts.SYSTEM_MESSAGE,
                       verbose: bool = False):
        super().__init__(model, api_key, debug=debug, system_message=system_message, verbose=False)
        self.space = space
        self.verbose = verbose
        self.generations = {}

    def summarize_meeting(self, transcript: str) -> MeetingSummary:
        summary: MeetingSummary = self(prompts.SUMMARIZE_TRANSCRIPT_PROMPT.format(transcript=transcript), 
                    structure=MeetingSummary,
                    context=self.space.__str__())
        self.generations['meeting_summary'] = summary
        return summary
    
    def generate_tasks(self, meeting_summary: MeetingSummary | None = None) -> MeetingTasks:
        if not meeting_summary:
            meeting_summary = self.generations.get('meeting_summary')
            if not meeting_summary:
                raise ValueError("Meeting Summary not provided or previously generated.")
        tasks: MeetingTasks = self(prompts.GENERATE_TASK_FOR_USER_PROMPT.format(user=self.space.user_name, meeting_summary=meeting_summary),
                    structure=MeetingTasks,
                    context=self.space.__str__())
        self.generations['tasks'] = tasks
        return tasks
    
    # Generate follow up tasks for the user based on the meeting
    def generate_follow_up_tasks(self, meeting_transcript: str) -> MeetingTasks:
        tasks: MeetingTasks = self(prompts.GENERATE_FOLLOW_UP_TASKS_PROMPT.format(user=self.space.user_name, transcript=meeting_transcript),
                    structure=MeetingTasks,
                    context=self.space.__str__())
        self.generations['follow_up_tasks'] = tasks
        return tasks
    
    # Generate email templates to send out to accomplish follow up tasks
    # Requires meeting summary and follow up tasks
    def generate_email_drafts(self, meeting_summary: MeetingSummary | None = None, follow_up_tasks: MeetingTasks | None = None) -> EmailDrafts:
        if not meeting_summary:
            meeting_summary = self.generations.get('meeting_summary')
            if not meeting_summary:
                raise ValueError("Meeting Summary not provided or previously generated.")
        if not follow_up_tasks:
            follow_up_tasks = self.generations.get('follow_up_tasks')
            if not follow_up_tasks:
                raise ValueError("Follow Up Tasks not provided or previously generated.")
        email_drafts: EmailDrafts = self(prompts.GENERATE_EMAIL_DRAFT_PROMPT.format(user=self.space.user_name, meeting_summary=meeting_summary, follow_up_tasks=follow_up_tasks),
                    structure=EmailDrafts,
                    context=self.space.__str__())
        return email_drafts
    
    
if __name__ == "__main__":
    space = Space(space_name="Weekly Meeting", user_name="James Dimon")

    # WITHOUT COMPANION
    # meeting_summarizer = GeminiClient()

    # with open("examples/sample_transcript.txt", "r") as f:
    #     transcript = f.read()

    # meeting_summary = meeting_summarizer(prompts.SUMMARIZE_TRANSCRIPT_PROMPT.format(transcript=transcript), 
    #                                      structure=MeetingSummary,
    #                                      context=space.__str__())
    # print("Meeting Summary:")
    # for point in meeting_summary.main_points:
    #     print("- " + point.point)
    # print()

    # WITH COMPANION
    companion = Companion(space)
    with open("examples/sample_transcript.txt", "r") as f:
        transcript = f.read()

    meeting_summary = companion.summarize_meeting(transcript)
    print("Meeting Summary:")
    for point in meeting_summary.main_points:
        print("- " + point.point)
    
    tasks = companion.generate_tasks(meeting_summary)
    print("Tasks:")
    for task in tasks.tasks:
        print(f"Task: {task.task}")
        print(f"Description: {task.description}")

    follow_up_tasks = companion.generate_follow_up_tasks(transcript)
    email_drafts = companion.generate_email_drafts(meeting_summary, follow_up_tasks)
    print("Email Drafts:")
    for email_draft in email_drafts.drafts:
        print(f"Recipient: {email_draft.recipient}")
        print(f"Subject: {email_draft.subject}")
        print(f"Body: {email_draft.body}")