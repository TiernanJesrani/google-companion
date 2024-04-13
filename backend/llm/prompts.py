SUMMARIZE_TRANSCRIPT_PROMPT = """
    Given the below transcript, succinctly summarize the main points of the conversation.
    Transcript:
    {transcript}
    Summary:
"""

GENERATE_TASK_FOR_USER_PROMPT = """
    Given the below meeting summary, generate a list of potential follow up tasks to be completed.

    Generate the tasks for the user {user}.

    Meeting Summary:
    {meeting_summary}

    Tasks:
"""

# check if there are follow up tasks before using this prompt
GENERATE_EMAIL_DRAFT_PROMPT = """
    Given the below meeting summary and list of follow up tasks, generate templates for any emails the user might need to send out to accomplish the follow up tasks.

    Generate the email drafts for the user {user}.

    Meeting Summary:
    {meeting_summary}

    Tasks:
    {tasks}

    Email Drafts:
"""