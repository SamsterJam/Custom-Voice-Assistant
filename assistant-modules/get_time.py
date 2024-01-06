from datetime import datetime

def get_time():
    # Get the current date and time
    current_datetime = datetime.now()

    # Convert the datetime to a string in ISO 8601 format
    datetime_str = current_datetime.isoformat()

    return datetime_str