from .views import DoctorsNoteViewSet
from django.urls import path

app_name = 'doctorsnote'


urlpatterns = [


    path('submit-note/', DoctorsNoteViewSet.as_view(
        {'post': 'submit_note'}), name='submit-note'),


    path('my-notes/', DoctorsNoteViewSet.as_view(
        {'get': 'my_notes'}), name='my-notes'),



]
