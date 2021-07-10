from django import template

register = template.Library()
from accounts.models import Product


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    return dict_data.get(str(key))


@register.filter('getprodname')
def getprodname(key):
    print(key)
    product = Product.objects.get(id=key)
    product_name = product.name
    return product_name


@register.filter('getprodprice')
def getprodprice(key):
    product = Product.objects.get(id=key)
    product_price = product.price
    return product_price


@register.filter('getprodamount')
def getprodamount(key,value):

    key=int(key)
    product = Product.objects.get(id=key)
    product_price = product.price
    return product_price*value


@register.filter('gettotalamount')
def gettotalamount(cart):
    print(cart)
    total = 0
    for i,val in cart:
        total = total + getprodamount(i,val)
    return total
