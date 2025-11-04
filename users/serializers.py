from djoser.serializers import UserCreateSerializer as BaseCreateSerializer, UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        fields=['id','email','password','first_name','last_name','address','phone_number']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
       ref_name='CustomUser'
       fields=['id','email','first_name','last_name','address','phone_number','is_staff']
       
       read_only_fields=['is_staff']
