import os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

internet_search = DuckDuckGoSearchRun()

@tool
def fetch_office_template(template_name: str) -> str:
    """
        template_name: The exact name of the file('leave_request' or 'meeting_invitation_email').
    """
    folder_path = "templates"
    file_path = os.path.join(folder_path, f"{template_name}.txt")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error reading the template file: {e}"
    else:
        return (
            f"Error: Template '{template_name}' not found. "
            f"Available templates are: leave_request, meeting_invitation_email."
        )

tools = [internet_search, fetch_office_template]