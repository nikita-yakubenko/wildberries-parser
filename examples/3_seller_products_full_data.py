"""
In this example we get first 100 products from seller and then get full data for all this products.
"""


from pprint import pprint

from wildberries_parser import WildberriesParser


# set seller id with you wanna work
seller_id = 4123

# how many products we wanna parse
max_products = 100

# select needed sorting
sorting = 'priceup'

# create parser object
WB_parser = WildberriesParser()

# get first 100 products from seller with "priceup" sorting
seller_products = WB_parser.get_products_by_seller(seller_id=seller_id, max_products=max_products, ordering=sorting)

# pretty print seller products data
pprint(seller_products)


# work with seller products short data if needed
...


# collect all got seller products ids to list
product_ids = [product['id'] for product in seller_products]

# get full products data
products_data = WB_parser.get_products_data(product_ids=product_ids)

# pretty print products data
pprint(products_data)


# or work with full products data
...
