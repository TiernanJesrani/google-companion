"""
Sample code for working with Gemini Chat and Gemini Embedding APIs
"""
from wrappers.gemini_chat import GeminiClient, GeminiClientWithMemory
from wrappers.gemini_embedding import GeminiEmbeddingClient
import schemas as schema
import prompts


# Example Usage
# Using https://www.marketbeat.com/earnings/transcripts/103443/
if __name__ == "__main__":
    meeting_summarizer = GeminiClient(structure=schema.MeetingSummary)
    task_generator = GeminiClient(structure=schema.MeetingTasks)
    email_draft_generator = GeminiClient(structure=schema.EmailDrafts)

    with open("sample_transcript.txt", "r") as f:
        transcript = f.read()
    
    meeting_summary = meeting_summarizer(prompts.SUMMARIZE_TRANSCRIPT_PROMPT.format(transcript=transcript))
    print("Meeting Summary:")
    # print(meeting_summary)
    for point in meeting_summary.main_points:
        print("- " + point.point)
    print()
    
    # tasks = task_generator(prompts.GENERATE_TASK_FOR_USER_PROMPT.format(user="James Dimon", meeting_summary=meeting_summary))
    # print("Tasks:")
    # for task in tasks.tasks:
    #     print(f"Task: {task.task}")
    #     print(f"Description: {task.description}")
    # print()

    follow_up_tasks = task_generator(prompts.GENERATE_FOLLOW_UP_TASKS_PROMPT.format(user="James Dimon", meeting_summary=meeting_summary))
    email_drafts = email_draft_generator(prompts.GENERATE_EMAIL_DRAFT_PROMPT.format(user="James Dimon", meeting_summary=meeting_summary, follow_up_tasks=follow_up_tasks))
    print("Email Drafts:")
    # print(email_drafts)
    for email_draft in email_drafts.drafts:
        print(f"Recipient: {email_draft.recipient}")
        print(f"Subject: {email_draft.subject}")
        print(f"Body: {email_draft.body}")
    print()