from .views import BookDoctorSerializerViewSet
from django.urls import path

app_name = 'booking'


urlpatterns = [


    path('available-doctors/', BookDoctorSerializerViewSet.as_view(
        {'get': 'available_doctors'}), name='available-doctors'),

    path('book-a-doctor/',
         BookDoctorSerializerViewSet.as_view({'post': 'book_doctor'}), name='book-a-doctor'),

    path('my-patients/',
         BookDoctorSerializerViewSet.as_view({'get': 'my_patients'}), name='my-patients'),

    path('close-booking/',
         BookDoctorSerializerViewSet.as_view({'post': 'close_booking'}), name='close-booking'),



]
