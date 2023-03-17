from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from kafka import KafkaProducer


class PromoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promo'
    verbose_name = _('promo code')

    def ready(self):
        from . import signals
        if (instance := getattr(settings, 'KAFKA_INSTANCE', None)) and hasattr(settings, 'KAFKA_TOPIC'):
            instance = instance if isinstance(instance, list) else [instance]
            signals.producer = KafkaProducer(bootstrap_servers=instance)
            post_save.connect(signals.send_message, sender='promo.PromoCode', dispatch_uid='send_message')
