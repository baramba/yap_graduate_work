import logging
from http import HTTPStatus

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BulkPromoCreate

loger = logging.getLogger(__name__)


@receiver(post_save, sender=BulkPromoCreate, dispatch_uid="send_bulk_request")
def send_request(instance, created, **kwargs):
    if not created:
        return
    # response = requests.get(getattr(settings, 'generator_url'), params={'id': instance.id})
    response = requests.get('http://flask:5000/api/v1/code_generator/id', params={'id': instance.id})
    if response.status_code != HTTPStatus.OK:
        loger.error('Generator returned not 200 status', response.json())
