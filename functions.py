import math
from datetime import datetime

def get_week_num(today, cc):
    # Determine the start and stop dates
    first_monday = datetime.strptime(cc.get('first_monday'), '%m/%d/%Y')
    last_date = datetime.strptime(cc.get('last_day'), '%m/%d/%Y')

    # Determine the current week number
    if today < first_monday:
        week_num = 1
    elif today > last_date:
        today = last_date
        delta_ms = today - first_monday
        delta_d = delta_ms.days
        week_num = int(math.floor((delta_d)/7+1))
    else:
        delta_ms = today - first_monday
        delta_d = delta_ms.days
        week_num = int(math.floor((delta_d)/7+1))

    return week_num
