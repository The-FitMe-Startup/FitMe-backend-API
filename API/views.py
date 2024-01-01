from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from knox.models import AuthToken
from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from API.serializers import UserSerializer, OutfitPostSerializer, ItemSerializer, CreateUserSerializer, \
    SubscriptionLevelSerializer, PieceTypeSerializer, MaterialSerializer, ProfileSerializer, \
    UpdateDeleteProfileSerializer
from API.models import OutfitPost, Item, SubscriptionLevel, PieceType, Material
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import mixins


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileUpdateAPI(mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateDeleteProfileSerializer


class OutfitPostViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    queryset = OutfitPost.objects.all().order_by('date_created')
    serializer_class = OutfitPostSerializer
    permission_classes = []  # permissions.IsAuthenticated]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = []


class SubscriptionLevelViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionLevel.objects.all()
    serializer_class = SubscriptionLevelSerializer
    permission_classes = []


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
