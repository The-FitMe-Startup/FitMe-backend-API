from django.contrib.auth.models import User
from rest_framework import serializers
from API.models import OutfitPost, Item, Material, PieceType, SubscriptionLevel, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'is_public', 'subscription_level', 'liked_outfits']
        # extra_kwargs = {'liked_outfits': {'read_only': True}}

    def get_fields(self):
        fields = super().get_fields()

        exclude_fields = self.context.get('exclude_fields', [])
        for field in exclude_fields:
            # providing a default prevents a KeyError
            # if the field does not exist
            fields.pop(field, default=None)

        return fields


class UserSerializer(serializers.ModelSerializer):
    outfitPosts = serializers.PrimaryKeyRelatedField(many=True, queryset=OutfitPost.objects.all())
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'outfitPosts', 'profile']


class UpdateDeleteProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile')

    def update(self, instance, validated_data):
        data = validated_data.get('profile')
        data.update({'subscription_level': data.get('subscription_level').id})
        serializer = ProfileSerializer(instance.profile, data=validated_data.get('profile'))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.save()
        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        profile_data = validated_data['profile']
        profile = Profile.objects.create(user=user, subscription_level=profile_data['subscription_level'],
                                         is_public=profile_data['is_public'])
        profile.save()
        return user


class OutfitPostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OutfitPost
        fields = '__all__'
        extra_kwargs = {'generated': {'read_only': True}, 'date_created': {'read_only': True}, 'total_price': {'read_only': True}}


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True}}


class SubscriptionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionLevel
        fields = '__all__'


class PieceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceType
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
