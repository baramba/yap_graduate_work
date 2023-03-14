import random
import string
import uuid

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class IdTimeMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True, editable=False)

    class Meta:
        abstract = True


class Product(IdTimeMixin):
    name = models.CharField(_('product name'), max_length=255, unique=True)
    description = models.CharField(_('product description'), max_length=512, blank=True, null=True)
    price = models.DecimalField(_('product price'), max_digits=9, decimal_places=2, default=0)

    class Meta:
        db_table = 'content\".\"product'
        ordering = ('name',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


class ProductPromoCode(IdTimeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    promo_code = models.ForeignKey('PromoCode', on_delete=models.CASCADE, null=True)
    bulk = models.ForeignKey('BulkPromoCreate', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'content\".\"product_promo'
        constraints = [
            models.UniqueConstraint(fields=('product', 'promo_code'), name='UniqProductPerPromo'),
            models.UniqueConstraint(fields=('product', 'bulk'), name='UniqProductPerBulk'),
            models.CheckConstraint(
                check=Q(promo_code__isnull=False) | Q(bulk__isnull=False),
                name='not_both_null'
            )
        ]
        verbose_name = _('related product')
        verbose_name_plural = _('related products')


class PromoCode(IdTimeMixin):
    class DiscountType(models.TextChoices):
        PRICE_FIX = 'fixed_price', _('fixed price')
        DISCOUNT_PERCENT = 'percentage_discount', _('percentage discount')
        DISCOUNT_FIX = 'fixed_discount', _('fixed discount')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    code = models.CharField('code', max_length=50, unique=True, db_index=True, blank=True,
                            help_text=_('leave blank for autofill'))
    start_at = models.DateTimeField(_('valid from'), blank=True, null=True)
    expired = models.DateTimeField(_('valid to'), blank=True, null=True)
    user_id = models.UUIDField(_('promo assign to user (UUID id)'), blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='promos', verbose_name=_('promo assign to products'),
                                      through=ProductPromoCode, blank=True)
    activates_possible = models.PositiveIntegerField(_('number of possible activations'), default=1)
    activates_left = models.PositiveIntegerField(_('number of activations left'), blank=True,
                                                 help_text=_('leave blank for autofill'))
    discount_type = models.CharField(_('discount type'), max_length=30, choices=DiscountType.choices)
    discount_amount = models.DecimalField(_('discount value'), max_digits=9, decimal_places=2)
    minimal_amount = models.DecimalField(_('minimum check amount to apply'), max_digits=9, decimal_places=2,
                                         default=0)
    is_active = models.BooleanField(_('promo code is active'), default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='codes', verbose_name=_('creator'))

    class Meta:
        db_table = 'content\".\"promo'
        ordering = ('-created',)
        verbose_name = _('promo')
        verbose_name_plural = _('promos')

    def __str__(self):
        return f'{self.title}, {self.description[:20]}, c:{self.start_at}, до:{self.expired}'

    def save(self, *args, **kwargs):
        if self.activates_left == None:
            self.activates_left = self.activates_possible

        if self.code != '':
            return super().save(*args, **kwargs)
        length = getattr(settings, 'promo_code_length', 20)
        while True:
            self.code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            try:
                return super().save(*args, **kwargs)
            except IntegrityError as e:
                if 'unique constraint' in e.args:
                    continue
                raise


class History(IdTimeMixin):
    promocode = models.ForeignKey(PromoCode, on_delete=models.PROTECT, related_name='history',
                                  verbose_name=_('activated promo'))
    applied_user_id = models.UUIDField(_('code is activated by (UUID id)'))
    discount_amount = models.DecimalField(_('amount of the applied discount'), max_digits=9, decimal_places=2)
    billing_info = models.TextField(_('info from billing service'), blank=True, null=True)

    class Meta:
        db_table = 'content\".\"history'
        ordering = ('-created',)
        verbose_name = _('activation log')
        verbose_name_plural = _('activations log')


class BulkPromoCreate(IdTimeMixin):
    creation_done = models.BooleanField(_('creation completed'), default=False)
    url_download = models.URLField(_('download csv link'), blank=True, null=True)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    start_at = models.DateTimeField(_('valid from'), blank=True, null=True)
    expired = models.DateTimeField(_('valid to'), blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='promos_bulk', verbose_name=_('promo assign to products'),
                                      through=ProductPromoCode, blank=True)
    discount_type = models.CharField(_('discount type'), max_length=30, choices=PromoCode.DiscountType.choices)
    discount_amount = models.DecimalField(_('discount value'), max_digits=9, decimal_places=2)
    minimal_amount = models.DecimalField(_('minimum check amount to apply'), max_digits=9, decimal_places=2,
                                         default=0)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bulks', verbose_name=_('creator'))

    class Meta:
        db_table = 'content\".\"bulk_creation'
        ordering = ('-created',)
        verbose_name = _('promo code generator')
        verbose_name_plural = _('promo codes generator')


@receiver(post_save, sender=BulkPromoCreate, dispatch_uid="send_bulk_request")
def send_request(instance, created, **kwargs):
    if created:
        requests.get('some')
