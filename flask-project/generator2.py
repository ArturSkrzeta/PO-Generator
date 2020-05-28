import json

with open('data.json') as json_f:
    purchase_order = json.load(json_f)

products = purchase_order['purchase-order']['products']
vendor = purchase_order['purchase-order']['vendor']
company = purchase_order['purchase-order']['company']
po_number = purchase_order['purchase-order']['po_number']

total = 0
for product in products:
    total += product['Price Each']*product['Quantity']

print(products)
