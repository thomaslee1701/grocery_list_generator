import csv
from dataclasses import dataclass
from collections import defaultdict
"""
Structure of the grocery list csv

product_name | quantity | location | notes

"""

@dataclass
class ShoppingItem:
    product_name: str
    quantity: str
    location: str
    notes: str

class GroceryList:
    columns = ('product_name', 'quantity', 'location', 'notes')

    def __init__(self, grocerycsv) -> None:
        self.shoppingItems = []
        self.shoppingListDict = defaultdict(list)
        self.parseGroceryXlsx(grocerycsv)
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
            newProduct.append(prod + ' ' * (maxProductNameLength - len(prod)) + '\t')
            newQuantities.append(quant + ' ' * (maxQuantitiesLength - len(quant)) + '\t\t')
            newNotes.append(note + ' ' * (maxNoteslist - len(note)))
        return newProduct, newQuantities, newNotes

    def exportShoppingListTxt(self):
        with open('GROCERYLIST.txt', 'w') as f:
            for loc, itemsList in self.shoppingListDict.items():
                f.write('-' * (len(loc) * 3) + '\n')
                f.write('-' * (len(loc)-1) + ' ' + loc.upper() + ' ' + '-' * (len(loc)-1) + '\n')
                f.write('-' * (len(loc) * 3) + '\n')
                productNames, quantities, notes = [item.product_name for item in itemsList], [item.quantity for item in itemsList], [item.notes for item in itemsList]
                for prod, quant, note in zip(*self.formatItemsText(productNames, quantities, notes)):
                    f.write(f'{prod}{quant}{note}\n')
                f.write('\n')

GL = GroceryList('grocery_list.csv')
GL.exportShoppingListTxt()
print('done!')

