from datetime import datetime

import pytz
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets, parsers, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from API.models import OutfitPost, Item, SubscriptionLevel, PieceType, Material, StyleTag
from API.permissions import IsSelfOrAdmin, IsSelf, IsAuthorOrReadAndCreateOnly, IsAdminOrReadOnly, \
    IsAuthenticatedToCreateOrReadOnly
from API.serializers import UserSerializer, OutfitPostSerializer, ItemSerializer, CreateUserSerializer, \
    SubscriptionLevelSerializer, PieceTypeSerializer, MaterialSerializer, ProfileSerializer, \
    UpdateDeleteProfileSerializer, StyleTagSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This view set automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]


class CreatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This view set automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.filter(is_superuser=False).filter(profile__is_public=True)
    serializer_class = UserSerializer
    permission_classes = []

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'exclude_fields': [
                'email'
            ]
        })
        return context


class ProfileUpdateAPI(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateDeleteProfileSerializer
    permission_classes = [IsSelf]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'exclude_fields': [
                'liked_outfits'
            ]
        })
        return context


class StyleTagViewSet(viewsets.ModelViewSet):
    queryset = StyleTag.objects.all()
    serializer_class = StyleTagSerializer
    permission_classes = [IsAuthenticatedToCreateOrReadOnly]


class OutfitPostViewSet(viewsets.ModelViewSet):
    queryset = OutfitPost.objects.filter(is_public=True).order_by('date_created')
    serializer_class = OutfitPostSerializer
    permission_classes = [IsAuthorOrReadAndCreateOnly]

    def perform_create(self, serializer):
        items = self.get_object().items
        print(items)
        total = 0
        for item in items:
            if item.price is not None:
                total += item.price

        generated = 'generated' in self.request.keys()

        serializer.save(author=self.request.user,
                        date_created=datetime.now(tz=pytz.UTC),
                        total_price=total,
                        generated=generated)

    @action(detail=True, methods=['post'], renderer_classes=[renderers.JSONRenderer])
    def like(self, request, *args, **kwargs):
        data = {
            'liked_outfits': [self.get_object().id]
        }
        serializer = ProfileSerializer(request.user.profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['get'], detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_closet_outfits(self, request, *args, **kwargs):
        outfits = OutfitPost.objects.filter(author=request.user)
        serializer = self.get_serializer(outfits, many=True)
        return Response(serializer.data)


class ItemViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [IsSelf]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['get'], detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_closet(self, request, *args, **kwargs):
        items = Item.objects.filter(owner=request.user)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)


class SubscriptionLevelViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionLevel.objects.all()
    serializer_class = SubscriptionLevelSerializer
    permission_classes = [IsAdminOrReadOnly]


class PieceTypeViewSet(viewsets.ModelViewSet):
    queryset = PieceType.objects.all()
    serializer_class = PieceTypeSerializer
    permission_classes = [IsAuthenticatedToCreateOrReadOnly]


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticatedToCreateOrReadOnly]


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # profileSerializer = ProfileSerializer(data=request.data)
        # profileSerializer.is_valid(raise_exception=True)
        user = serializer.save()
        # profileSerializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'exclude_fields': [
                'liked_outfits'
            ]
        })
        return context


class LoginAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            })
        else:
            return Response({"error": "Invalid credentials"})
