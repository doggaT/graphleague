from datetime import datetime


def get_time_since(date_time_obj):
    now = datetime.now()
    time_passed = now - date_time_obj

    days_passed = time_passed.days
    seconds_passed = time_passed.seconds

    if days_passed < 1:
        formatted_time = f"{seconds_passed // 3600} hours ago"
    elif days_passed == 1:
        formatted_time = f"{days_passed} day ago"
    else:
        formatted_time = f"{days_passed} days ago"

    return formatted_time
