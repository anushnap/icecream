import pandas as pd
import os

wd = os.getcwd()

# Import data
dairy_prod = pd.read_csv(wd + "/csv/dairy_indicators.csv")[['key', 'contains_dairy']]
organic_prod = pd.read_csv(wd + "/csv/organic_indicators.csv")[['key', 'CONTAINS_ORGANIC']]
products_working = pd.read_csv(wd + "/products_working.csv")
reviews = pd.read_csv(wd + "/data/reviews_updated_v2.csv")

# Merge product data
products_full = products_working \
    .merge(dairy_prod, how = 'left', on = 'key') \
    .merge(organic_prod, how = 'left', on = 'key')
products_full.rename(columns = {'CONTAINS_ORGANIC': 'contains_organic'}, inplace = True)

# Dummify contains_dairy and contains_organic
products_full['contains_dairy'] = products_full['contains_dairy'].apply(lambda x: 1 if (x is True) else 0)
products_full['contains_organic'] = products_full['contains_organic'].apply(lambda x: 1 if (x is True) else 0)

# Write to new csv
products_full.to_csv(wd + '/products_all_dummies.csv')

# Merge product data to reviews data
reviews_full = reviews \
    .merge(products_full.drop(columns = [
                                        'rating',
                                        'rating_count',
                                        'ingredients',
                                        'ingredients_as_list',
                                        'parent_ingredients_as_set', 
                                        'parent_ingredients_as_list',
                                        'Unnamed: 0',
                                        'subhead',
                                        'description'
                                        ]), how = 'left', on = 'key') \
    .drop(columns = reviews.columns[0])

reviews_full.to_csv(wd + '/reviews_with_dummies.csv')
print(reviews_full[['contains_dairy', 'contains_organic']].head())