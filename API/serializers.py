from django.contrib.auth.models import User
from rest_framework import serializers
from API.models import OutfitPost, Item, Material, PieceType, SubscriptionLevel, Profile


class UserSerializer(serializers.ModelSerializer):
    outfitPosts = serializers.PrimaryKeyRelatedField(many=True, queryset=OutfitPost.objects.all())
    profile = serializers.PrimaryKeyRelatedField(many=False, queryset=Profile.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'outfitPosts', 'profile']

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        None,
                                        validated_data['password'])
        return user

class OutfitPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = OutfitPost
        fields = ['author', 'items', 'generated']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'