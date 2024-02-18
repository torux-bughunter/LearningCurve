from django.urls import path
from core import views

urlpatterns = [
    path('goals/', views.goals_list, name='goals_list'),
    path('goals/create/', views.create_goal, name='create_goal'),
    path('goals/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('routines/create/', views.create_routine, name='create_routine'),
    path('calendar/', views.calendar, name='calendar'),
path('process_braindump/', views.process_braindump, name='process_braindump')
]