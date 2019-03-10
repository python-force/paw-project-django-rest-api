from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . views import UserRegisterView, RetrieveUpdateProfileView, UpdateUserDogView, NextDogView

# API endpoints
urlpatterns = format_suffix_patterns([
    path('api/user/login/', obtain_auth_token, name='login-user'),
    path('api/user/preferences/', RetrieveUpdateProfileView.as_view(), name='user-preferences'),
    path('api/user/', UserRegisterView.as_view(), name='register-user'),
    # path('api/profiles/', ListProfileView.as_view(), name='list-profiles'),
    # path('api/dog/-1/undecided/next/', RetrieveDogView.as_view(), name='dog-list'),
    path('api/dog/<str:pk>/<str:dog_filter>/next/', NextDogView.as_view(), name='dog-filter-detail'),
    path('api/dog/<str:pk>/<str:status>/', UpdateUserDogView.as_view(), name='dog-list'),
    path('favicon\.ico',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    path('', TemplateView.as_view(template_name='index.html'))
])
