import copy
import time,random
import uuid
from collections import namedtuple

# create the following variables
# order id
# seller id
# customer id

# 20 customer ids

customer_ids = [i for i in  range(0,20)]
seller_ids = [i for i in  range(0,4)]



# using named tuple to create product ids

Product = namedtuple(  typename= 'Product',
                    field_names=['product_id','product_name','price'])

product = [Product('cte01','pen','10'),
Product('cte02','rubber','5'),
Product('cte03','board','15')]

def get_orders():

    order_id = str(uuid.uuid1())
    customer_id = random.choice(customer_ids)
    seller_id = random.choice(seller_ids)
    product_o = []

    available_products = copy.copy(product)
    for p in range(0,len(product)-1):
        product_order = {}
        _  = random.choice(available_products)
        available_products.remove(_)
        product_order['qty'] = random.randint(1,20)

        product_order['product_id'] = _.product_id
        product_order['product_name'] = _.product_name
        product_order['price'] = _.price
        product_o.append(product_order)

    order = {}

    order['order_id'] =  order_id
    order['customer_id'] = customer_id
    order['seller_id']  = seller_id 
    order['product'] = product_o

    return order 





