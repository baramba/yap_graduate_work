# Generated by Django 4.1.7 on 2023-03-03 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Наименование продукта')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'db_table': 'content"."product',
            },
        ),
        migrations.CreateModel(
            name='ProductPromoCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promo.product')),
            ],
            options={
                'db_table': 'content"."product_promo',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('code', models.CharField(blank=True, db_index=True, help_text='Оставить пустым для автогенерации', max_length=50, unique=True, verbose_name='Код')),
                ('start_at', models.DateTimeField(verbose_name='Код действителен с')),
                ('expired', models.DateTimeField(verbose_name='Код действителен до')),
                ('user_id', models.UUIDField(blank=True, null=True, verbose_name='Код привязан к пользователю (UUID id)')),
                ('activates_possible', models.PositiveIntegerField(verbose_name='Количество возможных активаций')),
                ('activates_left', models.PositiveIntegerField(verbose_name='Количество оставшихся активаций')),
                ('discount_type', models.CharField(choices=[('fixed_price', 'фиксированная цена'), ('percentage_discount', 'скидка в процентах'), ('fixed_discount', 'фиксироанная скидка')], max_length=30, verbose_name='Тип лояльности')),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Размер скидки/фикса')),
                ('minimal_amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Минимальная сумма чека для применения скидки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Промокод активен и может быть активирован')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='codes', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('products', models.ManyToManyField(blank=True, related_name='promos', through='promo.ProductPromoCode', to='promo.product', verbose_name='Код привязан к продуктам')),
            ],
            options={
                'verbose_name': 'промокод',
                'verbose_name_plural': 'промокоды',
                'db_table': 'content"."promo',
            },
        ),
        migrations.AddField(
            model_name='productpromocode',
            name='promo_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promo.promocode'),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('applied_user_id', models.UUIDField(null=True, verbose_name='Код применен к пользователю (UUID id)')),
                ('discount_amount', models.DecimalField(decimal_places=2, editable=False, max_digits=9, verbose_name='Размер примененной скидки в валюте счета')),
                ('billing_info', models.TextField(verbose_name='Информация от сервиса оплаты')),
                ('promocode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='history', to='promo.promocode', verbose_name='Активированный промокод')),
            ],
            options={
                'verbose_name': 'история активации кода',
                'verbose_name_plural': 'история активаций кодов',
                'db_table': 'content"."history',
            },
        ),
    ]
