from django.db import models
from common.models import CommonModel

class Wishlist(CommonModel):

    """
    WishList Model Definition
    """

    # name = models.CharField(max_length=150),
    stores = models.ManyToManyField("stores.Store",
                                    related_name="wishlists", blank=True, null=True)
    user = models.OneToOneField("users.User", 
                            on_delete=models.CASCADE,
                            related_name="wishlists",)
