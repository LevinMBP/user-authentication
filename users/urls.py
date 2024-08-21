from django.urls import path, re_path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view()),
    path('user', UserView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('activate/<slug:uidb64>/<slug:token>', VerificationView.as_view(), name="activate"),
    # need to cover . and _
    re_path(r'^activate/(?P<uidb64>[A-Za-z0-9_\-]+)/(?P<token>[A-Za-z0-9._~-]+)$', VerificationView.as_view(), name="activate"),
]