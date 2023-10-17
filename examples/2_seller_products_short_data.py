"""
In this example we just get products short data from seller.
If you get products data by 'get_products_by_seller' - you receive short data for products.
If you need full data for products - use 'get_products_data' method as explained in 'get_products_data_by_ids.py' example.
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


# work with seller products data yourself
...
