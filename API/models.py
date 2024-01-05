from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class SubscriptionLevel(models.Model):
    title = models.CharField()
    description = models.CharField()


class Profile(models.Model):
    Budgets = {
        "LOW": "$0-100",
        "MID": "$100-300",
        "HIGH": "$300-500",
        "DESIGNER": "$500+"
    }  # tbd

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    subscription_level = models.ForeignKey(SubscriptionLevel, on_delete=models.CASCADE)
    liked_outfits = models.ManyToManyField("OutfitPost")  # using model that is not yet defined
    is_public = models.BooleanField(default=True)
    picture = models.ImageField(upload_to="images/profile-pictures/", null=True, blank=True)
    budget = models.CharField(choices=Budgets, null=True, blank=True)


class PieceType(models.Model):
    title = models.CharField()


class Material(models.Model):
    title = models.CharField()


class StyleTag(models.Model):
    title = models.CharField()


class Item(models.Model):
    owner = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="images/items/")
    brand = models.CharField()
    color = models.CharField() # can be filled out by AI
    type = models.ForeignKey(PieceType, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    style_tags = models.ManyToManyField(StyleTag)


class OutfitPost(models.Model):
    author = models.ForeignKey(User, related_name='outfitPosts', on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    generated = models.BooleanField(default=False)
    date_created = models.DateTimeField()
    picture = models.ImageField(upload_to="images/outfits/")
    total_price = models.IntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True)
    description = models.CharField(null=True, blank=True)
    style_tags = models.ManyToManyField(StyleTag)
    is_public = models.BooleanField()