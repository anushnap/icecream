import os
import pandas as pd
import numpy as np
import re

# Adds ingredients_as_list column to products dataframe containing list of comma-separated 
# discrete ingredients
def split_ingredients(products):
    products['ingredients_as_list'] = products['ingredients'].apply(lambda x: process_ingredients_to_list(x))
    products['parent_ingredients_as_list'] = products['ingredients_as_list'].apply(lambda x: get_parent(x))

    # for i in range(len(products)):
    #     ingr_i = products['ingredients'][i].lower()
    #     ingr_split = re.split(r'[.,]\s*(?![^()]*\))', ingr_i) # split on commas, ignore commas inside paren
    #     products['ingredients_as_list'][i] = ingr_split
        
    #     for i in ingr_split:
    #         if i.strip() not in ingr_dict:
    #             ingr_dict[i.strip()] = 1
    #         else:
    #             ingr_dict[i.strip()] += 1
    
    # return(ingr_dict)


def get_parent(ingr):
    return([i.split("(")[0].strip() for i in ingr])


# Split ingredients column on commas, ignoring commas within parentheses
def process_ingredients_to_list(ing_i):
    # ing_i = prod_ing_i.str.lower()
    return(re.split(r'[.,]\s*(?![^()]*\))', ing_i.lower()))


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



# Returns a split and tokenized ingredients column into parent and child columns
def split_parent_child(df_column):
    parent_child = df_column.str.split("(", expand = True)
    parent = parent_child[0].str.strip()
    child = parent_child[1].str.replace(")", "").str.strip()

    return(parent, child)


# Make dummy columns and add to products dataframe.
def make_dummies(products):
    # Make dummies for ingredients
    dummy_ingredients(products)

    # Make dummies for brand
    products = pd.get_dummies(data = products, columns = ['brand'])
    
    return(products)


# Create dummy variables for extras/toppings:
# - Peanuts
# - Almonds
# - Coffee
# - Strawberries
# - Raspberries
# - Pecans
# Others?
def dummy_ingredients(products):
    dummies = ['peanuts', 'almonds', 'pecans', 'coffee', 'strawberries', 'raspberries', 'walnuts', 'rum']

    # Create new column for each desired dummy
    for d in dummies:
        col_name = "contains_" + d
        products[col_name] = products['ingredients_as_list'].apply(lambda x: 1 if (d in x) else 0)


if __name__ == "__main__":
    wd = os.getcwd()
    products = pd.read_csv(wd + "/data/products.csv")
    
    split_ingredients(products)
    products = make_dummies(products)
    # ingr_dict = split_ingredients(products)
    # ingredients_df = make_ingredients_df(ingr_dict)
    # ingredients_df.to_csv(wd + "/data/ingredients.csv")
    # print(ingredients_df)
    
    products.to_csv(wd + "/products_working.csv")

    