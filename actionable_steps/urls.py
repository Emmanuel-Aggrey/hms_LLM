from actionable_steps.views import ActionableTaskViewSet


from django.urls import path

app_name = 'actionable_steps'


urlpatterns = [


    path('active_tasks/', ActionableTaskViewSet.as_view(
        {'get': 'active_tasks'}), name='active-tasks'),

    path('mark-as-completed/',
         ActionableTaskViewSet.as_view({'post': 'mark_as_completed'}), name='mark-as-completed'),




]
