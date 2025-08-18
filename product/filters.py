from django_filters.rest_framework import FilterSet
from product.models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields={
            'category_id':['exact'], # category id deva and 
            'price':['gt','lt'] # genic page pries high to low dkano holo ....
        }