
from accounts import views
from rest_framework.routers import DefaultRouter
from django.urls import path


app_name = 'account'


router = DefaultRouter()
router.register("", views.UserSerializerView)


urlpatterns = [

    path('availablity', views.UserAvailabilitySerializer.as_view(), name='availablity')



]


urlpatterns += router.urls
