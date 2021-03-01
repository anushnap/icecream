import pandas as pd
import os

wd = os.getcwd()

# Import data
dairy_prod = pd.read_csv(wd + "/csv/dairy_indicators.csv")[['key', 'contains_dairy']]
organic_prod = pd.read_csv(wd + "/csv/organic_indicators.csv")[['key', 'CONTAINS_ORGANIC']]
products_working = pd.read_csv(wd + "/products_working.csv")

# Merge data
products_full = products_working.merge(dairy_prod, how = 'left', on = 'key').merge(organic_prod, how = 'left', on = 'key')
products_full.rename(columns = {'CONTAINS_ORGANIC': 'contains_organic'}, inplace = True)

# Write to new csv
products_full.to_csv(wd + '/products_all_dummies.csv')