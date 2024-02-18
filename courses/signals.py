# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from moviepy.editor import VideoFileClip
from .models import Episode, Course
import mercadopago
from django.conf import settings
import json

sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

@receiver(post_save, sender=Episode)
def update_episode_duration(sender, instance, **kwargs):
    if not instance.duration:
        try:
            with VideoFileClip(instance.video.path) as video:
                duration = int(video.duration)
                instance.duration = duration
                instance.save(update_fields=['duration'])
        except Exception as e:
            print(f"Error calculating duration for {instance.title}: {e}")

@receiver(post_save, sender=Course)
def update_course_preference(sender, instance, **kwargs):
    if not instance.preference:
        preference_data = {
            "items": [
                {
                    "id": instance.pk,
                    "title": instance.title,
                    "quantity": 1,
                    "unit_price": float(instance.price),
                    "currency_id": "PEN",
                }
            ],
            "back_urls": {
                "success": settings.CSRF_TRUSTED_ORIGINS[1],
                # "failure": "https://www.failure.com",
                # "pending": "https://www.pending.com"
            },
            "auto_return": "approved",
            "notification_url": f"{settings.CSRF_TRUSTED_ORIGINS[1]}/course/mercado_pago_webhook/",
            "expires": False,
            "statement_descriptor": "Worstat",
            "binary_mode": True,
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        instance.preference = json.dumps(preference)
        print(instance.preference)
        instance.save(update_fields=['preference'])
