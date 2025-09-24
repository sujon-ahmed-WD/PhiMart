from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category,Review,ProductImage
from product.serializers import ProductSerializers,CategoriesSerializers,ReviewSerializers
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from product.paginations import DefaultPagination
from rest_framework.permissions import DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from api.permissions import IsAdminOrReadOnly,FullDjangoModelPermission
from product.permissions import IsReviewAuthorOrReadonly
from product.serializers import ProductImageSerializers,ProductSerializers
from .permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema


# jodi pagination sob jaga show korta chi tah hola pagination setinge.py set korta hova  korta hova
class ProductViewSet(ModelViewSet):      
    queryset=Product.objects.all()
    serializer_class=ProductSerializers
    
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]  # Generic faltering ...........
    filterset_class = ProductFilter
    pagination_class=DefaultPagination
    search_fields =['name','description']
    ordering_fields=['price','updated_at']
    permission_classes=[IsReviewAuthorOrReadonly]
@swagger_auto_schema(
                operation_summary="Create a product by admin",
                operation_description="This allow an admin to create a product",
                request_body=ProductSerializers,
                responses={
                    201: ProductSerializers,
                    400: "Bad Request"
                }
            )
def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
        serializer_class=ProductImageSerializers
        permission_classes=[IsReviewAuthorOrReadonly]  
        
        def get_queryset(self):
             return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
        def perform_create(self,serializer):
                    serializer.save(product_id=self.kwargs.get('product_pk'))
""" self.kwargs['product_pk']

            👉 URL থেকে product-এর id টেনে আনে।
            উদাহরণ: /products/5/images/ দিলে এখানে 5 দেওয়া যাবে।
            
            ProductImage.objects.filter(product_id=...)
            👉 ProductImage টেবিল থেকে শুধু সেই লাইনগুলো (rows) খুঁজে বের করে, গুলো ওই product_id এর সাথে মিলে।
            
            """


           
class CategoryViewSet(ModelViewSet): # --------> this is model_view_Set
    queryset=Category.objects.annotate(
    product_count=Count('products')).all()
    serializer_class=CategoriesSerializers
    permission_classes=[IsAdminOrReadOnly]
    
    
  #   
class ReviewSet(ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes=[IsReviewAuthorOrReadonly]

    
    def perform_create(self,serializer): # Review save kora jonno 
        serializer.save(user=self.request.user)
    def perform_update(self,serializer): # ja user login object golo 
        serializer.save(user=self.request.user)
    
    def get_queryset(self): #  REview show korar jono 
         return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
     
    def get_serializer_context(self):
        return {"product_id": self.kwargs.get('product_pk')}
    
        # if getattr(self, 'swagger_fake_view', False):
        #     return {}

      