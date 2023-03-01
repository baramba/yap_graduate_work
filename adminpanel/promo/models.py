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


class ProductThrough(IdTimeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promocode = models.ForeignKey('PromoCode', on_delete=models.CASCADE)


class PromoCode(IdTimeMixin):
    class DiscountType(models.TextChoices):
        PRICE_FIX = 'fixed_price', 'фиксированная цена'
        DISCOUNT_PERCENT = 'percentage_discount', 'скидка в процентах'
        DISCOUNT_FIX = 'fixed_discount', 'фиксироанная скидка'

    title = models.CharField('Название', max_length=255, blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    code = models.CharField('Код', max_length=50)
    start_at = models.DateTimeField('Код действителен с')
    expired = models.DateTimeField('Код действителен до')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promos',
                                verbose_name='Код привязан к пользователю', blank=True, null=True)
    product_ids = models.ManyToManyField(Product, related_name='promos', verbose_name='Код привязан к продуктам',
                                         through=ProductThrough, blank=True)
    activates_possible = models.PositiveIntegerField('Количество возможных активаций')
    activates_left = models.PositiveIntegerField('Количество оставшихся активаций')
    discount_type = models.CharField('Тип лояльности', max_length=30, choices=DiscountType.choices)
