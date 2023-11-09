from dateutil.relativedelta import relativedelta
import plotly.express as px
import calendar
from datetime import datetime, timedelta
import pandas as pd

trange = []
cmonth = datetime(2023, 4, 1)
for i in range(7):
    cmonths = cmonth+relativedelta(months=i+1)
    trange.append(cmonths)
# Define the starting date

now = datetime.now()

for c in trange:
    if c.month == now.month and c.day < now.day:
        print('True')
print(cmonth.date)

print(now)

# Sample list
my_list = [10, 20, 30, 40, 50]
print(sum(my_list))
# Define the condition
"""
condition = lambda x: x > 30

# Find the first element that matches the condition and its location
for index, element in enumerate(my_list):
    if condition(element):
        print(f"Found element {element} at index {index}")
        break
else:
    print("No element matching the condition found")


# Count the number of elements that satisfy the condition
count = sum(1 for element in my_list if condition(element))

# Print the count
print(count)


# Get the current date
current_date = datetime.now()

# Get the number of days in the current month
_, num_days = calendar.monthrange(current_date.year, current_date.month)

# Generate a list of all dates in the current month
dates_in_month = [current_date.replace(day=day) for day in range(1, num_days + 1)]

# Print the dates
for date in dates_in_month:
    print(date)

month=datetime.now()

for i in range(7):
    print(month-relativedelta(months=i))
"""
