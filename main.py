# Student Name: Thomas Ghebray
# PSID: 1889967


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import datetime


# product class object
class Product:
    # parameterized constructor
    def __init__(self, pId, mName, pType, damaged):
        self.p_id = pId
        self.m_name = mName
        self.p_type = pType
        self.damaged = damaged
        self.price = 0.0
        self.s_date = datetime.date.today()

    # allow for printing of the object,
    # Only manufacturer name, product tyApe and price are printed
    def to_string(self, message):
        print(message + self.m_name + " " + self.p_type + ", price: " + str(self.price))


# allow for sorting
def sort_by_price(product):
    return product.price


# Creating List
manufacturers = []
products = dict()
productTypes = []
alternates = []


def create_dictionaries():
    # Opening file and adding to products
    with open('ManufacturerList.csv', 'r') as manuList:
        reader = csv.reader(manuList)
        for row in reader:
            # product id, manufacturer, type, damaged or not damaged
            product = Product(int(row[0]), str(row[1]).strip(), str(row[2]).strip(), str(row[3]).strip() == 'damaged')
            products[int(row[0])] = product
            # add to manufacturers and types if they are not
            # already present
            if row[1] not in manufacturers:
                manufacturers.append(product.m_name)
            if row[2] not in productTypes:
                productTypes.append(product.p_type)

    # Updating prices of current products in inventory
    with open('PriceList.csv', 'r') as plist:
        price = csv.reader(plist)
        for row in price:
            # update/set product prices
            products[int(row[0])].price = float(row[1])

    # add service dates to products in inventory
    with open('ServiceDatesList.csv', 'r') as dates_list:
        service = csv.reader(dates_list)
        for row in service:
            curr_date = str(row[1]).split('/')
            service_date = datetime.date(int(curr_date[2]), int(curr_date[0]), int(curr_date[1]))
            products[int(row[0])].s_date = service_date


# main function to find a product
# takes in two arguments, the manufacturer and the product type
def find_product(manu, prod_type):
    found_products = []
    alternates.clear()
    for key in products.keys():
        item = products[key]
        # Find products (manufacturer, item type, etc)
        if item.m_name.lower() == manu.lower() and item.p_type.lower() == prod_type.lower() and\
                item.s_date > datetime.date.today() and item.damaged is False:
            found_products.append(item)
        # if it is the same type, include among alternatives
        elif item.p_type.lower() == prod_type.lower() and item.s_date > datetime.date.today() and item.damaged is False:
            alternates.append(item)
    # no found products, print no such items
    if len(found_products) == 0:
        print("No such item in inventory")
        return

    # sort by price descending, then get the first element, the maximum price
    found_products.sort(key=sort_by_price, reverse=True)
    found_products[0].to_string("Your item is: ")

    # find alternatives based on current alternatives and current product
    find_alternatives(alternates, found_products[0])


"""
this method finds the closest alternative from another manufacturer
:param all alternatives with same time
:param current selected product
"""


def find_alternatives(alts, product):
    # if there is one object, print it,
    # saves computational time
    if len(alts) == 1:
        alts[0].to_string("You may also consider: ")
    if len(alternates) > 1:
        # find the closest alternative
        diff = 99999
        closest = None
        for i in range(len(alts)):
            # abs gets the absolute value of difference
            difference = abs(alts[i].price - product.price)
            # comparing price values
            if difference < diff:
                diff = difference
                closest = alternates[i]
        closest.to_string("You may also consider: ")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create inventory
    create_dictionaries()
    while True:
        command = str(input('Enter the manufacturer name and item type or enter "q" to exit: '))
        if command == "q" or command == "Q":
            break
        elif command:
            manufacturer = command.split(" ")[0]
            productType = command.split(" ")[1]
            if manufacturer is None or productType is None:
                print("No such item in inventory")
            else:
                find_product(manufacturer, productType)


