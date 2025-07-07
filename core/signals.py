"""
    Create a signal that automatically deduct the quantity product sold from the initial total quantity.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from core.forms import ProductForm
from core.models import Product, Sale, User, UserProfile


@receiver(post_save, sender=Sale)
def total_quantity_handler(sender, instance, created, **kwargs):
    if created:
        product = get_object_or_404(Product, name=instance)
        product.quantity -= instance.quantity
        form = ProductForm(instance=product)
        if form.is_valid():
            form.save()
            return "Total quantity for product has been updated."
        return "Total quantity for product could not be updated due to invalid form."


@receiver(post_save, sender=User)
def user_profile_handler(sender, instance, created, **kwargs):
    if created:
        userProfile = UserProfile.objects.create(user=instance)
        userProfile.save()
        return userProfile
