# admin_dashboard/urls.py
from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.dashboard_home, name='home'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<str:report_id>/', views.complaint_detail, name='complaint_detail'),
    # --- NEW: Delete Complaint URL ---
    path('complaints/delete/<str:report_id>/', views.delete_complaint, name='delete_complaint'),
    # --- END NEW ---
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('export-complaints/', views.export_complaints, name='export_complaints'),
    path('monthly-summary/', views.monthly_summary_report, name='monthly_summary_report'),

    # --- New Contractor Management URLs ---
    path('contractors/', views.contractor_list, name='contractor_list'),
    # --- THIS LINE IS NOW FIXED (added comma) ---
    path('contractors/add/', views.add_contractor, name='add_contractor'), 
    path('contractors/edit/<int:contractor_id>/', views.edit_contractor, name='edit_contractor'),
    path('contractors/delete/<int:contractor_id>/', views.delete_contractor, name='delete_contractor'),
    path('contractors/analytics/', views.contractor_analytics, name='contractor_analytics'),
]