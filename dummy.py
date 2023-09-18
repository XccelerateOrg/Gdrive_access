import pandas as pd

df = pd.DataFrame({'Week 1': [60, 60, 40, None], 'Week 2': [60, 40, 29, None], 'Week 3': [None, 60, 40, 45]},
                    index=['Amy', 'Betty', 'Cathiee', 'David'])
df["Count"] = 0*len(df.index)
df. fillna(0, inplace=True)

lst1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
lst2 = ['a', 'b', 'c']
c = pd.MultiIndex.from_product([lst1, lst2])

print(len(c)%3)