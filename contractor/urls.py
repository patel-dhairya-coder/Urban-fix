# contractor/urls.py
from django.urls import path
from . import views

app_name = 'contractor'

urlpatterns = [
    path('login/', views.contractor_login, name='login'),
    path('logout/', views.contractor_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('', views.dashboard, name='dashboard'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<str:report_id>/', views.complaint_detail, name='complaint_detail'),
]
