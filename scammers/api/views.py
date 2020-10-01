from rest_framework.generics import (
ListAPIView,RetrieveAPIView,
UpdateAPIView, DestroyAPIView,
CreateAPIView, GenericAPIView
) 
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework.response import Response
from knox.models import AuthToken
from scammers.models import Scammer,Images
from .serializers import(
ScammerListSerializer, ScammerDetailSerializer,
ScammerCreateSerializer,
ImageCreateSerializer, RegisterSerializer,
UserSerializer,LoginSerializer
) 
from django.http import HttpResponse
import django_filters.rest_framework
class ScammerListAPIView(ListAPIView):
    queryset = Scammer.objects.all()
    serializer_class = ScammerListSerializer
    

    def get_queryset(self,*args,**kwargs):
        lower_limit = int(self.request.query_params.get('lower_limit',0))
        upper_limit = int(self.request.query_params.get('upper_limit',200))
        #if 'lower_limit' in self.request.query_params and 'upper_limit' in self.request.query_params:
            #lower_limit = int('lower_limit')
            #upper_limit = int('upper_limit')
            #return super().get_queryset(*args,**kwargs)[lower_limit:upper_limit]
        #else:
        return super().get_queryset(*args,**kwargs)[lower_limit:upper_limit]


class ScammerFilterAPIView(ListAPIView):
    serializer_class = ScammerListSerializer
    queryset = Scammer.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['phone']


class ScammerDetailAPIView(RetrieveAPIView):
    queryset = Scammer.objects.all()
    serializer_class = ScammerDetailSerializer


class ScammerUpdateAPIView(UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Scammer.objects.all()
    serializer_class = ScammerDetailSerializer

class ScammerDeleteAPIView(DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = Scammer.objects.all()
    serializer_class = ScammerDetailSerializer


class ScammerCreateAPIView(CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Scammer.objects.all()
    serializer_class = ScammerCreateSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Scammer was successfully added to our database',
            'data': response.data
        })

class ImageCreateAPIView(CreateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageCreateSerializer



class RegisterUserAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("valid serializer")
        user = serializer.save()
        return Response({
        'user' : UserSerializer(user,context=self.get_serializer_context()).data,
        'token' : AuthToken.objects.create(user)[1]
        })
        #return Response(serializer.errors)

       

    def get(self,request,*args,**kwargs):
        return HttpResponse("Helllo world")


class LoginUserAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if hasattr(user,'is_authenticated'):
            print("INSIDE IS AUTHENTICATED")
            return Response({
            'user' : UserSerializer(user,context=self.get_serializer_context()).data,
            'token' : AuthToken.objects.create(user)[1]
            })
        
        raise user
    

class UserAPI(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user



class ScammersCountAPIView(APIView):
    """
    A view that returns the count of active users.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        scammers_count = Scammer.objects.count()
        content = {'scammers_count': scammers_count}
        return Response(content)