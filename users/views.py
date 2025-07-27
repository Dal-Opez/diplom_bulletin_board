from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django_rest_passwordreset.views import ResetPasswordConfirm, ResetPasswordRequestToken
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework import status


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomResetPasswordConfirm(ResetPasswordConfirm):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if not token:
            return Response(
                {"error": "Token parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "status": "success",
            "message": "Token is valid",
            "instructions": {
                "method": "POST",
                "url": "/users/reset_password/confirm/",
                "body_params": {
                    "token": token,
                    "password": "your_new_password"
                }
            }
        }, status=status.HTTP_200_OK)


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    pass