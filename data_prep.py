import os
import pandas as pd
import numpy as np
import re

# Adds ingredients_as_list column to products dataframe containing list of comma-separated 
# discrete ingredients
def split_ingredients(products):
    products['ingredients_as_list'] = products['ingredients'].apply(lambda x: process_ingredients_to_list(x))
    products['parent_ingredients_as_list'] = products['ingredients_as_list'].apply(lambda x: get_parent(x))
    products['parent_ingredients_as_set'] = products['parent_ingredients_as_list'].apply(lambda x: set(x))


def get_parent(ingr):
    return([i.split("(")[0].strip() for i in ingr])


# Split ingredients column on commas, ignoring commas within parentheses
# Ignore extra descriptors in ingredients list. 
# Ex] 'Chocolate Ice Cream: Cream' in ingredients will return ['cream'] in list
def process_ingredients_to_list(ing_i):
    initial_ingredients_list = re.split(r'[.,]\s*(?![^()]*\))', ing_i.lower())
    removed_colons_list = []
    for i in initial_ingredients_list:
        if ":" in i:
            removed_colons_list.append(i.split(":")[1].strip())
        else:
            removed_colons_list.append(i)

    return(removed_colons_list)


# Makes ingredients dataframe with occurrence count in products dataframe
# Adds parent and child columns for ingredients where parent is ingredient prior to parentheses
# Ex: LIQUID SUGAR (SUGAR, WATER): Parent is LIQUID SUGAR, child is SUGAR, WATER
def make_ingredients_df():
    ingredients_dict = {}

    products['parent_ingredients_as_set'].apply(lambda x: get_ingredients_keys(x, ingredients_dict))
    for ingr in ingredients_dict.keys():
        products['parent_ingredients_as_set'].apply(lambda x: increment_ingredients_dict(x, ingredients_dict, ingr))

    ingr_df = pd.DataFrame(ingredients_dict.keys(), columns = ['Parent Ingredient'])
    ingr_df['count'] = ingredients_dict.values()
    ingr_df['percent_containing'] = ingr_df['count'] / len(products)

    return(ingr_df)


def get_ingredients_keys(parent_list, ingredients_dict):
    for i in parent_list:
        if i not in ingredients_dict.keys():
            ingredients_dict[i] = 1


def increment_ingredients_dict(parent_list, ingredients_dict, ingredient_key):
    if ingredient_key in parent_list:
        ingredients_dict[ingredient_key] += 1


# Make dummy columns and add to products dataframe.
def make_dummies(products):
    # Make dummies for ingredients
    dummy_topping(products)

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
def dummy_topping(products):
    dummies = ['peanuts', 'almonds', 'pecans', 'coffee', 'strawberries', 'raspberries', 'walnuts', 'rum', 'toffee']

    # Create new column for each desired dummy
    for d in dummies:
        col_name = "contains_" + d
        products[col_name] = products['parent_ingredients_as_set'].apply(lambda x: 1 if (d in x) else 0)


if __name__ == "__main__":
    wd = os.getcwd()
    products = pd.read_csv(wd + "/data/products.csv")
    
    split_ingredients(products)
    products = make_dummies(products)
    products.to_csv(wd + "/products_working.csv")
    ingredients_analysis = make_ingredients_df()
    ingredients_analysis.to_csv(wd + "/ingredients.csv")
    