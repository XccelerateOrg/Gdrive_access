import itertools
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Two sample lists
list1 = [1, 2]
list2 = ['a', 'b', 'c']

# Perform Cartesian product
cartesian_product = list(itertools.product(list1, list2))

# Print the Cartesian product
df = pd.DataFrame({
    'Name': ['John', 'Alice', 'Bob', 'Emily'],
    'Age': [25, 30, 35, 28],
    'City': ['New York', 'London', 'Paris', 'Sydney']
})
