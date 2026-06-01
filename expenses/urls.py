from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groups/<int:group_pk>/expenses/new/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/', views.expense_detail, name='expense_detail'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('groups/<int:group_pk>/settle/', views.settlement_create, name='settlement_create'),
    path('settlements/<int:pk>/confirm/', views.settlement_confirm, name='settlement_confirm'),
]
