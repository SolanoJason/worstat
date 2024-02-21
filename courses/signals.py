# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Episode, Course
import mercadopago
from django.conf import settings
import cv2
import datetime
import json

sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

@receiver(post_save, sender=Episode)
def update_episode_duration(sender, instance, **kwargs):
    print('SIGNALSIGNALSIGNALSIGNALSIGNALSIGNALSIGNALSIGNALSIGNAL')
    if not instance.duration:
        data = cv2.VideoCapture(instance.video.url)
        # count the number of frames 
        print(f'{data=}')
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT) 
        print(f'{frames=}')
        fps = data.get(cv2.CAP_PROP_FPS)
        print(f'{fps=}')
        seconds = round(frames / fps) 
        print(f'{seconds=}')
        instance.duration = seconds
        instance.save(update_fields=['duration'])

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
