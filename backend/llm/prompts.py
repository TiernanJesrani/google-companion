
SYSTEM_MESSAGE = """
    You are Google Companion, a helpful virtual assistant aiding users with organizing their Google Workspace meetings, tasks, emails, documents, etc.

    You have access to a "Space," which groups together zero-to-many calendar events, emails, documents, etc.

    You can generate meeting summaries, tasks, email drafts, etc. using the context of the space you are in.
"""

SUMMARIZE_TRANSCRIPT_PROMPT = """
    Given the below transcript, succinctly summarize the main points of the conversation.
    Transcript:
    {transcript}
    Summary:
"""

# After obtaining summary, task generation might not make sense - dynamically determine if there are tasks to generate
GENERATE_TASK_FOR_USER_PROMPT = """
    Given the below meeting summary, generate a list of potential follow up tasks to be completed.

    Generate the tasks specifically for the user {user}.

    Meeting Summary:
    {meeting_summary}

    Tasks:
"""

GENERATE_FOLLOW_UP_TASKS_PROMPT = """
    Given the below meeting transcript, generate a list of potential follow up tasks to be completed.

    Generate the follow ups specifically for the user {user}.

    Meeting:
    {transcript}

    Tasks:
"""

# Check if there are follow up tasks before using this prompt
GENERATE_EMAIL_DRAFT_PROMPT = """
    Given the below meeting summary and list of follow up tasks, generate templates for any emails the user might need to send out to accomplish the follow up tasks.

    Generate the email drafts for the user {user}.

    Meeting Summary:
    {meeting_summary}

    Tasks:
    {follow_up_tasks}

    Email Drafts:
"""