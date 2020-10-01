
from rest_framework import serializers
from django.contrib.auth import authenticate
from scammers.models import Scammer, Images, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    print("Inside serializer")
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password']

        extra_kwargs = {"password": {"write_only" : True} }


    def create(self,validated_data):
        email = validated_data.get("email")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        password = validated_data.get("password")

        user = User.objects.create_user(email=email,first_name=first_name,last_name=last_name,password=password)
        return user



class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self,data):
        try:
            user = authenticate(**data)
        except:
            raise ValidationError(
             _('Invalid value: Email or password'),
            code='invalid',
            )
        if user and user.is_active:
            return user
        return serializers.ValidationError("Incorrect credentials")

        
class ScammerListSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_fullname')
    url = serializers.HyperlinkedIdentityField(view_name='scammers-api:scammer_detail')
    class Meta:
        model = Scammer
        fields = ['id', 'url', 'title', 'phone', 'address', 'full_name']


    def get_fullname(self,obj):
        return f'{obj.first_name} {obj.last_name}'


class ScammerDetailSerializer(serializers.ModelSerializer):
    
    image_urls = serializers.SerializerMethodField('get_image_url')
    class Meta:
        
        model = Scammer
        fields = ['title', 'phone', 'address','details','image_urls']
        
        
    def get_image_url(self,obj):
        request = self.context.get("request")
        uris = []
        for img in obj.image_proofs.all():
            print(img)
            uris.append(request.build_absolute_uri(img.image.url))
        return uris




class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']



class ScammerCreateSerializer(serializers.ModelSerializer):
    image_proofs = ImageCreateSerializer(many=True,read_only=True)
    class Meta:
        model = Scammer
        fields = ['first_name','last_name','phone','address','title','details','image_proofs']

    def create(self, validated_data):
         print(self.context['request'].data)
         images_data = self.context['request'].FILES
         scammer = Scammer.objects.create(
             first_name=validated_data.get('first_name'),
             last_name= validated_data.get('last_name'),
             phone = validated_data.get("phone"),
             address = validated_data.get('address'),
             title = validated_data.get('title'),
             posted_by = self.context['request'].user,
             details = validated_data.get("details")
         )
         for image_data in images_data.values():
            print(image_data)
            Images.objects.create(scammer=scammer, image=image_data)
         return scammer


