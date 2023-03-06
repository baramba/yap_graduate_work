import random
import string
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db import models

User = get_user_model()


class IdTimeMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField('Создан', auto_now_add=True, editable=False)
    modified = models.DateTimeField('Изменен', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Product(IdTimeMixin):
    name = models.CharField('Наименование продукта', max_length=255, unique=True)
    description = models.CharField('Описание краткое', max_length=512, blank=True, null=True)
    price = models.DecimalField('Стоимость полная', max_digits=9, decimal_places=2, default=0)

    class Meta:
        db_table = 'content\".\"product'
        ordering = ('name',)
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.name


class ProductPromoCode(IdTimeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    promo_code = models.ForeignKey('PromoCode', on_delete=models.CASCADE)

    class Meta:
        db_table = 'content\".\"product_promo'
        constraints = [
            models.UniqueConstraint(fields=('product', 'promo_code'), name='UniqProductPerPromo'),
        ]
        verbose_name = 'привязанный продукт'
        verbose_name_plural = 'привязанные продукты'


class PromoCode(IdTimeMixin):
    class DiscountType(models.TextChoices):
        PRICE_FIX = 'fixed_price', 'фиксированная цена'
        DISCOUNT_PERCENT = 'percentage_discount', 'скидка в процентах'
        DISCOUNT_FIX = 'fixed_discount', 'фиксироанная скидка'

    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True, null=True)
    code = models.CharField('Код', max_length=50, unique=True, db_index=True, blank=True,
                            help_text='Оставить пустым для автогенерации')
    start_at = models.DateTimeField('Код действителен с', blank=True, null=True)
    expired = models.DateTimeField('Код действителен до', blank=True, null=True)
    user_id = models.UUIDField('Код привязан к пользователю (UUID id)', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='promos', verbose_name='Код привязан к продуктам',
                                      through=ProductPromoCode, blank=True)
    activates_possible = models.PositiveIntegerField('Количество возможных активаций')
    activates_left = models.PositiveIntegerField('Количество оставшихся активаций', blank=True,
                                                 help_text='Оставьте пустым для автоподстановки')
    discount_type = models.CharField('Тип лояльности', max_length=30, choices=DiscountType.choices)
    discount_amount = models.DecimalField('Размер скидки/фикса', max_digits=9, decimal_places=2)
    minimal_amount = models.DecimalField('Минимальная сумма чека для применения скидки', max_digits=9, decimal_places=2,
                                         default=0)
    is_active = models.BooleanField('Промокод активен и может быть активирован', default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='codes', verbose_name='Создатель')

    class Meta:
        db_table = 'content\".\"promo'
        ordering = ('-created',)
        verbose_name = 'промокод'
        verbose_name_plural = 'промокоды'

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
                                  verbose_name='Активированный промокод')
    applied_user_id = models.UUIDField('Код применен пользователем (UUID id)')
    discount_amount = models.DecimalField('Размер примененной скидки в валюте счета', max_digits=9, decimal_places=2)
    billing_info = models.TextField('Информация от сервиса оплаты', blank=True, null=True)

    class Meta:
        db_table = 'content\".\"history'
        ordering = ('-created',)
        verbose_name = 'история активации кода'
        verbose_name_plural = 'история активаций кодов'
