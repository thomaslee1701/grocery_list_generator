import pandas as pd

grocery_df = pd.read_excel('grocery_list.xlsx')

"""
Structure of the grocery list xlsx

Product Name | Quantity | Location | Notes

"""

def pad_string(s, pad_length):
    return s + ' ' * (pad_length - len(s))

# Remove all entries with quantity 0 or N/A
grocery_df = grocery_df[(~pd.isna(grocery_df['Quantity'])) & (~(grocery_df['Quantity']==0))]

location_names = grocery_df['Location'].dropna().unique()

# Write to the txt file
f = open('list.txt', 'w')
f.close()

with open('list.txt', 'a') as f:
    for location in location_names:
        grocery_df_temp = grocery_df[grocery_df['Location'] == location]
        product_names = grocery_df_temp['Product Name']
        grocery_df_temp = grocery_df_temp.set_index('Product Name')
        biggest_product_name = max([len(name) for name in product_names])
        f.write(f'--------------------\n{location.upper()}\n')
        for name in product_names:
            sr = grocery_df_temp.loc[name]
            quantity = sr['Quantity']
            if type(quantity) != str and quantity % 1 == 0:
                quantity = int(quantity)
            notes = sr['Notes']
            f.write(f'{pad_string(name, biggest_product_name + 4)} {pad_string(str(quantity), 6)} {notes} \n')
        f.write('--------------------\n\n')    
    # Now all the ones with no location specified
    grocery_df_temp = grocery_df[~(grocery_df['Location'].isin(location_names))]    
    product_names = grocery_df_temp['Product Name']
    grocery_df_temp = grocery_df_temp.set_index('Product Name')
    biggest_product_name = max([len(name) for name in product_names])
    for name in product_names:
        sr = grocery_df_temp.loc[name]
        quantity = sr['Quantity']
        if type(quantity) != str and quantity % 1 == 0:
            quantity = int(quantity)
        notes = sr['Notes']
        f.write(f'{pad_string(name, biggest_product_name + 4)} {pad_string(str(quantity), 6)} {notes} \n')

print('done!')

