from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('new/', views.group_create, name='group_create'),
    path('enter/', views.group_enter, name='group_enter'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('<int:pk>/dashboard/', views.group_dashboard, name='group_dashboard'),
    path('<int:pk>/leave/', views.group_leave, name='group_leave'),
    path('join/<uuid:token>/', views.group_join, name='group_join'),
]
