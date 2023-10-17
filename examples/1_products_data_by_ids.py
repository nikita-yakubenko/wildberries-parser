"""
In this example we get full products data by ids.
"""


from pprint import pprint

from wildberries_parser import WildberriesParser


# provide products ids who are you need to parse
product_ids = [15398837, 49903424, 8056582]

# create parser object
WB_parser = WildberriesParser()

# get full products data
products_data = WB_parser.get_products_data(product_ids=product_ids)

# pretty print products data
pprint(products_data)


# work with products data yourself
...
