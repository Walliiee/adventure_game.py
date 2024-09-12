import datetime
from bday_message import random_message

today = datetime.date.today()
next_bday = datetime.date(2024, 9, 10)

time_difference = next_bday - today

if today == next_bday:
    print(random_message)
else:
    print(f"Sorry, today is not your birthday. Your birthday is in {time_difference.days} days.")

