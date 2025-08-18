from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category,Review
from product.serializers import ProductSerializers,CategoriesSerializers,ReviewSerializers
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
# from rest_framework.pagination import PageNumberPagination
from product.paginations import DefaultPagination

# jodi pagination sob jaga show korta chi tah hola pagination setinge korta hova
class ProductViewSet(ModelViewSet):  
    queryset=Product.objects.all()
    serializer_class=ProductSerializers
    
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter] # Genric feltaringe ...........
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    search_fields =['name','description','category__name']
    ordering_fields=['price','updated_at']

         

    def destroy(self, request, *args, **kwargs): # ata modelviewsetup customize korsa
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product with stock more than 10 could not be deleted"})
        self.perform_destroy(product) # save korsa ata .....
        return Response(status=status.HTTP_204_NO_CONTENT)    
class CategoryViewSet(ModelViewSet): # --------> this is model_view_Set
    queryset=Category.objects.annotate(
        product_count=Count('products')).all()
    serializer_class=CategoriesSerializers
    
class ReviewSet(ModelViewSet):
    serializer_class = ReviewSerializers

    # def get_queryset(self):
    #     return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_queryset(self): #  REview show korar jono 
         return Review.objects.filter(product_id=self.kwargs['product_pk'])
     
    def get_serializer_context(self): 
        return  {'product_id':self.kwargs['product_pk']}
    

      