import csv
import os
from dataclasses import dataclass
from collections import defaultdict
"""
Structure of the grocery list csv

product_name | quantity | location | notes

"""
TITLE = """   _____   _____     ____     _____   ______   _____   __     __    _        _____    _____   _______ 
  / ____| |  __ \   / __ \   / ____| |  ____| |  __ \  \ \   / /   | |      |_   _|  / ____| |__   __|
 | |  __  | |__) | | |  | | | |      | |__    | |__) |  \ \_/ /    | |        | |   | (___      | |   
 | | |_ | |  _  /  | |  | | | |      |  __|   |  _  /    \   /     | |        | |    \___ \     | |   
 | |__| | | | \ \  | |__| | | |____  | |____  | | \ \     | |      | |____   _| |_   ____) |    | |   
  \_____| |_|  \_\  \____/   \_____| |______| |_|  \_\    |_|      |______| |_____| |_____/     |_|
     
"""

CREDITS = """
CREATED BY: THOMAS LEE
"""

@dataclass
class ShoppingItem:
    product_name: str
    quantity: str
    location: str
    notes: str

class GroceryList:
    columns = ('product_name', 'quantity', 'location', 'notes')

    def __init__(self, fullpath, groceryCsvName) -> None:
        self.fullpath = fullpath
        self.shoppingItems = []
        self.shoppingListDict = defaultdict(list)
        self.parseGroceryXlsx(fullpath + '\\' + groceryCsvName)
        self.initializeShoppingListDict(self.shoppingItems)
          
    def parseGroceryXlsx(self, grocerycsv):
        with open(grocerycsv, newline='') as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader: # Don't want to read in column names row
                attrs = dict((col, val) for col, val in zip(self.columns, row))
                if attrs['quantity'] != '0' and attrs['quantity'] != '':
                    self.shoppingItems.append(ShoppingItem(**attrs))
    
    def initializeShoppingListDict(self, shoppingItems):
        for item in shoppingItems:
            self.shoppingListDict[item.location].append(item)


    def formatItemsText(self, productNamesList, quantitiesList, notesList):
        """Returns three lists with properly padded words

        """
        maxProductNameLength = len(max(productNamesList, key=len))
        maxQuantitiesLength = len(max(quantitiesList, key=len))
        maxNoteslist = len(max(notesList, key=len))
        newProduct, newQuantities, newNotes = [], [], []
        for prod, quant, note in zip(productNamesList, quantitiesList, notesList):
            newProduct.append(prod + ' ' * (maxProductNameLength - len(prod)) + ' '*3)
            newQuantities.append(quant + ' ' * (maxQuantitiesLength - len(quant)) + ' '*6)
            newNotes.append(note + ' ' * (maxNoteslist - len(note)))
        return newProduct, newQuantities, newNotes

    def formatLocationsText(self, location):
        s = ''
        s += '-' * (len(location) * 3) + '\n'
        s += '-' * (len(location)-1) + ' ' + location.upper() + ' ' + '-' * (len(location)-1) + '\n'
        s += '-' * (len(location) * 3) + '\n'
        return s
    def exportShoppingListTxt(self):
        path = self.fullpath + '\\' + 'GROCERYLIST.txt'
        with open(path, 'w') as f:
            f.write(TITLE)
            for loc, itemsList in self.shoppingListDict.items():
                f.write(self.formatLocationsText(loc))
                productNames, quantities, notes = [item.product_name for item in itemsList], [item.quantity for item in itemsList], [item.notes for item in itemsList]
                for prod, quant, note in zip(*self.formatItemsText(productNames, quantities, notes)):
                    f.write(f'{prod}{quant}{note}\n')
                f.write('\n')
            f.write(CREDITS)
fullpath = os.path.dirname(os.path.realpath(__file__))
GL = GroceryList(fullpath, 'grocery_list.csv')
try:
    GL.exportShoppingListTxt()
except Exception as e:
    print(e)
    input()
print('done!')

