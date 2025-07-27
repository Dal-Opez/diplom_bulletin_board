from rest_framework import serializers
from .models import Advertisement, Review
from users.serializers import UserSerializer

class AdvertisementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

    def validate(self, attrs):
        if self.instance and self.instance.author != self.context['request'].user and not self.context['request'].user.is_staff:
            raise serializers.ValidationError("Вы можете редактировать только свои объявления")
        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    advertisement = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'advertisement']

    def create(self, validated_data):
        validated_data['advertisement_id'] = self.context['view'].kwargs['advertisement_id']
        return super().create(validated_data)

    def validate(self, attrs):
        if self.instance and self.instance.author != self.context['request'].user and not self.context['request'].user.is_staff:
            raise serializers.ValidationError("Вы можете редактировать только свои отзывы")
        return attrs