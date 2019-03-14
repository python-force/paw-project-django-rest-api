from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . views import (UserRegisterView,
                     RetrieveUpdateProfileView,
                     UpdateUserDogView,
                     NextDogView,
                     ListCreateDog,
                     RetrieveUpdateDog)

# API endpoints
urlpatterns = format_suffix_patterns([
    path('api/user/login/', obtain_auth_token, name='login-user'),
    path('api/user/preferences/',
         RetrieveUpdateProfileView.as_view(), name='user-preferences'),
    path('api/user/', UserRegisterView.as_view(), name='register-user'),
    path('api/dog/<str:pk>/update',
         RetrieveUpdateDog.as_view(), name='update-dog'),
    path('api/dog/', ListCreateDog.as_view(), name='create-dog'),
    path('api/dog/<str:pk>/<str:dog_filter>/next/',
         NextDogView.as_view(), name='dog-filter-detail'),
    path('api/dog/<str:pk>/<str:status>/',
         UpdateUserDogView.as_view(), name='dog-list'),
    path('favicon\.ico',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    path('', TemplateView.as_view(template_name='index.html'))
])
