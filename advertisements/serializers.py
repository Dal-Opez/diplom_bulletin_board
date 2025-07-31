from rest_framework import serializers
from .models import Advertisement, Review
from users.serializers import UserSerializer


class AdvertisementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = "__all__"
        read_only_fields = ["author", "created_at"]

    def validate(self, attrs):
        if self.instance:  # Проверка только при обновлении существующего объявления
            request = self.context.get("request")
            if request and request.user:
                if not (
                    self.instance.author == request.user
                    or request.user.is_staff
                    or request.user.role == "ADMIN"
                ):
                    raise serializers.ValidationError(
                        "Вы можете редактировать только свои объявления"
                    )
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    advertisement = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["author", "created_at", "advertisement"]

    def create(self, validated_data):
        validated_data["advertisement_id"] = self.context["view"].kwargs[
            "advertisement_id"
        ]
        return super().create(validated_data)

    def validate(self, attrs):
        if self.instance:  # Проверка только при обновлении существующего отзыва
            request = self.context.get("request")
            if request and request.user:
                # Аналогичная проверка прав как для объявлений
                if not (
                    self.instance.author == request.user
                    or request.user.is_staff
                    or request.user.role == "ADMIN"
                ):
                    raise serializers.ValidationError(
                        "Вы можете редактировать только свои отзывы"
                    )
        return attrs
