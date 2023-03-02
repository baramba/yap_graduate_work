import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class IdTimeMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(IdTimeMixin):
    name = models.CharField('Наименование продукта', max_length=255)

    class Meta:
        db_table = 'content\".\"product'
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class ProductPromoCode(IdTimeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promo_code = models.ForeignKey('PromoCode', on_delete=models.CASCADE)

    class Meta:
        db_table = 'content\".\"product_promo'


class PromoCode(IdTimeMixin):
    class DiscountType(models.TextChoices):
        PRICE_FIX = 'fixed_price', 'фиксированная цена'
        DISCOUNT_PERCENT = 'percentage_discount', 'скидка в процентах'
        DISCOUNT_FIX = 'fixed_discount', 'фиксироанная скидка'

    title = models.CharField('Название', max_length=255, blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    code = models.CharField('Код', max_length=50, unique=True, db_index=True)
    start_at = models.DateTimeField('Код действителен с')
    expired = models.DateTimeField('Код действителен до')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promos',
                                verbose_name='Код привязан к пользователю', blank=True, null=True)
    product_ids = models.ManyToManyField(Product, related_name='promos', verbose_name='Код привязан к продуктам',
                                         through=ProductPromoCode, blank=True)
    activates_possible = models.PositiveIntegerField('Количество возможных активаций')
    activates_left = models.PositiveIntegerField('Количество оставшихся активаций')
    discount_type = models.CharField('Тип лояльности', max_length=30, choices=DiscountType.choices)
    discount_amount = models.DecimalField('Размер скидки/фикса', decimal_places=2)

    class Meta:
        db_table = 'content\".\"promo'
        verbose_name = 'промокод'
        verbose_name_plural = 'промокоды'


class History(IdTimeMixin):
    promocode = models.ForeignKey(PromoCode, on_delete=models.PROTECT, related_name='history',
                                  verbose_name='Активированный промокод')
    applied_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='history',
                                        verbose_name='Промокод применен к пользователю')
    discount_amount = models.DecimalField('Размер примененной скидки в валюте счета', decimal_places=2, editable=False)
    billing_info = models.TextField('Информация от сервиса оплаты')

    class Meta:
        db_table = 'content\".\"history'
        verbose_name = 'история активации кода'
        verbose_name_plural = 'история активаций кодов'