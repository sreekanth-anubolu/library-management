from datetime import datetime, timedelta

def add_delta(days=3):
    curr_date = datetime.now().date()
    delta = timedelta(days=days)
    delta_date = curr_date + delta
    return delta_date

