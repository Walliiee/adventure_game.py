"""
Birthday countdown demo. Set BIRTHDAY_MONTH and BIRTHDAY_DAY for the target date.
"""
import datetime
from bday_message import random_message

# Configure the birthday (month=1-12, day=1-31)
BIRTHDAY_MONTH = 9
BIRTHDAY_DAY = 10

today = datetime.date.today()
# Use this year, or next year if the date has already passed
next_bday = datetime.date(today.year, BIRTHDAY_MONTH, BIRTHDAY_DAY)
if next_bday < today:
    next_bday = datetime.date(today.year + 1, BIRTHDAY_MONTH, BIRTHDAY_DAY)

time_difference = next_bday - today

if today == next_bday:
    print(random_message)
else:
    print(f"Sorry, today is not your birthday. Your birthday is in {time_difference.days} days.")

