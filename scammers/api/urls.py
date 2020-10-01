from django.urls import path,include
from .views import (
ScammerListAPIView,ScammerDetailAPIView,
ScammerUpdateAPIView, ScammerDeleteAPIView,
ScammerCreateAPIView,
ImageCreateAPIView, RegisterUserAPIView,
LoginUserAPIView,ScammerFilterAPIView,
ScammersCountAPIView, UserAPI
) 
from knox import views as knox_views
from knox.views import LogoutView
import knox.urls
app_name = "scammers_api"

urlpatterns = [
    path('scammers',ScammerListAPIView.as_view(),name="scammers_list"),
    path('scammers/filter',ScammerFilterAPIView.as_view(),name='scammer_filter'),
    path('scammers/<int:pk>',ScammerDetailAPIView.as_view(),name="scammer_detail"),
    path('scammers/<int:pk>/delete',ScammerDeleteAPIView.as_view(),name="scammer_delete"),
    path('scammers/<int:pk>/update',ScammerUpdateAPIView.as_view(),name="scammer_update"),
    path('scammers/create',ScammerCreateAPIView.as_view(),name="scammer_create"),
    path('scammers/create/images',ImageCreateAPIView.as_view(),name="image_create"),
    path('scammers/scammers_count',ScammersCountAPIView.as_view(),name="scammers_count"),
    path('auth',include(knox.urls)),
    path('auth/register',RegisterUserAPIView.as_view()),
    path('auth/login',LoginUserAPIView.as_view()),
    path('auth/logout',LogoutView.as_view(),name="knox_logout"),
    path('auth/user',UserAPI.as_view(),name="user"),
    
]


