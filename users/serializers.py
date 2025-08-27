from djoser.serializers import UserCreateSerializer as BaseCreateSerializer,UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        fields=['id','email','password','first_name','last_name','address','phone_number']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
       fields=['id','email','first_name','last_name','address','phone_number']
