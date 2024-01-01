from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class SubscriptionLevel(models.Model):
    title = models.CharField()
    description = models.CharField()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    subscription_level = models.ForeignKey(SubscriptionLevel, on_delete=models.CASCADE)
    liked_outfits = models.ManyToManyField("OutfitPost")  # using model that is not yet defined
    is_public = models.BooleanField(default=True)

"""@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()"""

class PieceType(models.Model):
    title = models.CharField()


class Material(models.Model):
    title = models.CharField()


class Item(models.Model):
    owner = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="images/")
    brand = models.CharField()
    color = models.CharField()
    type = models.OneToOneField(PieceType, on_delete=models.CASCADE)
    material = models.OneToOneField(Material, on_delete=models.CASCADE)


class OutfitPost(models.Model):
    author = models.ForeignKey(User, related_name='outfitPosts', on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    generated = models.BooleanField(default=False)
    date_created = models.DateTimeField()
