from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    # renvoie access & refresh token
    path('login/', TokenObtainPairView.as_view()),  
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    
]