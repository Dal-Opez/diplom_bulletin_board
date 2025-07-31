from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# from django_rest_passwordreset.views import (
#     ResetPasswordConfirm,
#     ResetPasswordRequestToken,
# )
from .views import (
    UserCreateView,
    CustomTokenObtainPairView,
    CustomResetPasswordConfirm,
    CustomResetPasswordRequestToken,
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "reset_password/",
        CustomResetPasswordRequestToken.as_view(),
        name="reset-password",
    ),
    path(
        "reset_password/confirm/",
        CustomResetPasswordConfirm.as_view(),
        name="reset-password-confirm",
    ),
]
