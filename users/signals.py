from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from wishlists.models import Wishlist

@receiver(post_save, sender=User)
def create_wishlist_for_new_user(sender, instance, created, **kwargs):
    """
    새로운 사용자가 생성될 때 위시리스트를 자동으로 생성하는 신호 핸들러
    """
    if created:
        Wishlist.objects.create(user=instance)