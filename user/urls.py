from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
# --- API Router ---
# The router will handle all URLs for the ComplaintViewSet under the 'api/' prefix
router = DefaultRouter()
router.register(r'complaints', views.ComplaintViewSet, basename='complaint')

# --- URL Patterns ---
urlpatterns = [
    # 1. Original Website URLs
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('report/', views.report, name="report"),
    path("track/", views.track_complaint, name="track"),
    path('role_select/', views.role_select, name='role_select'),
    # 2. API URLs (now grouped under 'api/')
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Include the router-generated URLs under the 'api/' prefix
    path('api/', include(router.urls)),
]