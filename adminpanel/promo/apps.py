from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from kafka import KafkaProducer


class PromoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promo'
    verbose_name = _('promo code')

    def ready(self):
        from django.conf import settings

        from . import signals
        from .models import BulkPromoCreate, PromoCode
        if getattr(settings, 'generator_url', None):
            post_save.connect(signals.send_request, sender=BulkPromoCreate, dispatch_uid='send_bulk_request')
        if not (instance := getattr(settings, 'kafka_instance', None)) or not getattr(settings, 'kafka_topic', None):
            return
        instance = instance if isinstance(instance, list) else [instance]
        signals.producer = KafkaProducer(bootstrap_servers=instance)
        post_save.connect(signals.send_message, sender=PromoCode, dispatch_uid='send_message')
