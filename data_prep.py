import os
import pandas as pd
import numpy as np
import re

def split_ingredients(products):
    ingr_dict = {}
    products['ingredients_as_list'] = np.nan # Create new col with list of ingredients

    for i in range(len(products)):
        ingr_i = products['ingredients'][i].lower()
        ingr_split = re.split(r'[.,]\s*(?![^()]*\))', ingr_i) # split on commas, ignore commas inside paren
        products['ingredients_as_list'][i] = ingr_split
        
        for i in ingr_split:
            if i.strip() not in ingr_dict:
                ingr_dict[i.strip()] = 1
            else:
                ingr_dict[i.strip()] += 1
    
    return(ingr_dict)


# Makes ingredients dataframe with occurrence count in products dataframe
# Adds parent and child columns for ingredients where parent is ingredient prior to parentheses
# Ex: LIQUID SUGAR (SUGAR, WATER): Parent is LIQUID SUGAR, child is SUGAR, WATER
def make_ingredients_df(dict):
    ingr_df = pd.DataFrame(ingr_dict.keys(), columns = ['Ingredient'])
    ingr_df['count'] = ingr_dict.values()
    ingr_df['percent_containing'] = ingr_df['count'] / len(products)

    # Split ingredients for parent/child ingredients
    ingr_df['Parent'], ingr_df['Child'] = split_parent_child(ingr_df['Ingredient'])

    return(ingr_df)


# Splits an ingredients column into parent and child columns and returns
def split_parent_child(df_column):
    parent_child = df_column.str.split("(", expand = True)
    parent = parent_child[0].str.strip()
    child = parent_child[1].str.replace(")", "").str.strip()

    return(parent, child)


# Create dummy variables for ingredients:
# - Cocoa vs. chocolate?
# - Peanuts
# - Almonds
# - Coffee
# - Strawberries
# - Raspberries
# - Pecans
# What others?
def dummy_ingredients(products):
    dummies = ['peanuts', 'almonds', 'pecans', 'coffee', 'strawberries', 'raspberries']

    # Create new column for each desired dummy
    for d in dummies:
        col_name = "contains_" + d
        products[col_name] = products['ingredients_as_list'].apply(lambda x: d in x)
        # Uncomment to see how many unique ice creams contain the dummy ingredient
        # print(products[col_name].sum())

def contains_choc(products):
    pass


def contains_cocoa(products):
    pass



if __name__ == "__main__":
    wd = os.getcwd()
    products = pd.read_csv(wd + "/data/products.csv")

    ingr_dict = split_ingredients(products)
    ingredients_df = make_ingredients_df(ingr_dict)
    # ingredients_df.to_csv(wd + "/data/ingredients.csv")
    # print(ingredients_df)
    dummy_ingredients(products)

    