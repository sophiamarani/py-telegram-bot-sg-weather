from datetime import datetime

def convert_iso_to_readable_date(iso_date_str):
    """
    Converts an ISO 8601 datetime string to a readable date format 'DD Mon YYYY'.

    Args:
        iso_date_str (str): The ISO 8601 datetime string. For example, '2024-12-18T00:00:00+08:00'.

    Returns:
        str: The formatted date string.
    """
    # Parse the ISO 8601 string to a datetime object
    datetime_obj = datetime.fromisoformat(iso_date_str)
    # Format the datetime object to the desired format
    return datetime_obj.strftime("%d %b %Y")

def bold_text(text):
    # Use Telegram's Markdown format for bold text
    return f"*{text}*"
