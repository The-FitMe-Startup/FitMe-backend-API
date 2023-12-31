from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from API import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'outfitPosts', views.OutfitPostViewSet, basename='outfitPost')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'items', views.ItemViewSet, basename='item')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
