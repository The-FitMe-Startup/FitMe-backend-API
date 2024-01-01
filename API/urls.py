from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from API import views
from API.views import RegistrationAPI, LoginAPI, ProfileUpdateAPI

from knox import views as knox_views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'outfit_posts', views.OutfitPostViewSet, basename='outfitPost')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profile_update', views.ProfileUpdateAPI, basename='profileUpdate')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'materials', views.MaterialViewSet, basename='material')
router.register(r'subscription_level', views.SubscriptionLevelViewSet, basename='subscriptionLevel')
router.register(r'piece_type', views.PieceTypeViewSet, basename='pieceType')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += format_suffix_patterns([
    path('register/', RegistrationAPI.as_view()),
    path('api/auth', include('knox.urls')),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/logout/all', knox_views.LogoutAllView.as_view(), name='knox_logout_all'),
    path('login/', LoginAPI.as_view(), name='knox-login'),
])
