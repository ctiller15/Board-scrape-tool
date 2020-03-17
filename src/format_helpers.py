days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def format_date(date_obj):
    return f"{days[date_obj.weekday()]}, {date_obj.day}/{date_obj.month}/{date_obj.year}"
