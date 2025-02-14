from django.urls import path
from .views import (
    UserSignupView,
    EmailPasswordLoginView,)


app_name = 'authentication'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),


    path('login/',
         EmailPasswordLoginView.as_view(), name='email_password'),



]
