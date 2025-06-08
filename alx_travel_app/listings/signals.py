from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Booking, Listing
from decimal import Decimal


@receiver(pre_save, sender=Booking)
def calculate_total_price(sender, instance, **kwargs):
    """
    Calculate total price for a booking before saving
    """
    if instance.listing and instance.check_in and instance.check_out:
        duration = (instance.check_out - instance.check_in).days
        if duration > 0:
            instance.total_price = instance.listing.price_per_night * Decimal(duration)


@receiver(post_save, sender=Booking)
def send_booking_notification(sender, instance, created, **kwargs):
    """
    Send notification when a booking is created or updated
    This is where you would integrate with email service, SMS, etc.
    """
    if created:
        # Here you would typically send email/SMS notifications
        # For now, we'll just print to console
        print(f"New booking created: {instance.id} for {instance.listing.title}")
    else:
        print(f"Booking updated: {instance.id} - Status: {instance.status}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create user profile or perform other actions when a user is created
    """
    if created:
        print(f"New user registered: {instance.username}")
