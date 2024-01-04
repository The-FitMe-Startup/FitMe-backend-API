from datetime import datetime
import pytz
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.views.decorators.csrf import csrf_exempt
from knox.models import AuthToken
from rest_framework import permissions, viewsets, parsers, renderers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from API.permissions import IsSelfOrAdmin, IsSelf, IsAuthorOrReadAndCreateOnly, IsAdminOrReadOnly
from API.serializers import UserSerializer, OutfitPostSerializer, ItemSerializer, CreateUserSerializer, \
    SubscriptionLevelSerializer, PieceTypeSerializer, MaterialSerializer, ProfileSerializer, \
    UpdateDeleteProfileSerializer, StyleTagSerializer
from API.models import OutfitPost, Item, SubscriptionLevel, PieceType, Material, StyleTag
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import mixins


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,IsSelfOrAdmin]

class CreatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
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

class ProfileUpdateAPI(mixins.UpdateModelMixin,
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OutfitPostViewSet(viewsets.ModelViewSet):
    queryset = OutfitPost.objects.all().order_by('date_created')
    serializer_class = OutfitPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadAndCreateOnly]

    def perform_create(self, serializer):
        items = self.get_object().items
        print(items)
        total = 0
        for item in items:
            if item.price is not None:
                total+=item.price

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


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionLevelViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionLevel.objects.all()
    serializer_class = SubscriptionLevelSerializer
    permission_classes = [IsAdminOrReadOnly]


class PieceTypeViewSet(viewsets.ModelViewSet):
    queryset = PieceType.objects.all()
    serializer_class = PieceTypeSerializer
    permission_classes = []


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = []


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
