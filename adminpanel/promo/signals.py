import logging
from http import HTTPStatus

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from kafka import KafkaProducer

from .models import BulkPromoCreate, PromoCode

logger = logging.getLogger(__name__)
producer: None | KafkaProducer = None


@receiver(post_save, sender=BulkPromoCreate)
def send_request(sender, instance: BulkPromoCreate, created, **kwargs):
    if not created:
        return
    response = requests.get(settings.GENERATOR_URL, params={'id': instance.id})
    if response.status_code != HTTPStatus.OK:
        logger.error('Generator returned not 200 status', response.json())


def send_message(sender, instance: PromoCode, created, **kwargs):
    if not created and not instance.user_id:
        return
    value = {
        'products': [product.name for product in instance.products] if instance.products else None,
        'type': instance.discount_type.label,
        'value': instance.discount_amount
    }
    producer.send(
        topic=settings.kafka_topic,
        key=instance.user_id,
        value=value,
    )
    logger.info('Message to kafka send')
