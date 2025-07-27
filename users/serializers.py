from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import USER

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "role",
            "avatar",
        )
        extra_kwargs = {
            "role": {"read_only": True},
            "password": {"write_only": True},
            "avatar": {"required": False},
        }

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.phone = validated_data["phone"]
        user.avatar = validated_data.get("avatar")
        user.role = USER
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token
