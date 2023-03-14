# Generated by Django 4.1.7 on 2023-03-14 10:42

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
            name='BulkPromoCreate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('creation_done', models.BooleanField(default=False, verbose_name='creation completed')),
                ('url_download', models.URLField(blank=True, null=True, verbose_name='download csv link')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('start_at', models.DateTimeField(blank=True, null=True, verbose_name='valid from')),
                ('expired', models.DateTimeField(blank=True, null=True, verbose_name='valid to')),
                ('discount_type', models.CharField(choices=[('fixed_price', 'fixed price'), ('percentage_discount', 'percentage discount'), ('fixed_discount', 'fixed discount')], max_length=30, verbose_name='discount type')),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='discount value')),
                ('minimal_amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='minimum check amount to apply')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bulks', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name': 'promo code generator',
                'verbose_name_plural': 'promo codes generator',
                'db_table': 'content"."bulk_creation',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='product name')),
                ('description', models.CharField(blank=True, max_length=512, null=True, verbose_name='product description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='product price')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'content"."product',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductPromoCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('bulk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='promo.bulkpromocreate')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promo.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'related product',
                'verbose_name_plural': 'related products',
                'db_table': 'content"."product_promo',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('code', models.CharField(blank=True, db_index=True, help_text='leave blank for autofill', max_length=50, unique=True, verbose_name='code')),
                ('start_at', models.DateTimeField(blank=True, null=True, verbose_name='valid from')),
                ('expired', models.DateTimeField(blank=True, null=True, verbose_name='valid to')),
                ('user_id', models.UUIDField(blank=True, null=True, verbose_name='promo assign to user (UUID id)')),
                ('activates_possible', models.PositiveIntegerField(default=1, verbose_name='number of possible activations')),
                ('activates_left', models.PositiveIntegerField(blank=True, help_text='leave blank for autofill', verbose_name='number of activations left')),
                ('discount_type', models.CharField(choices=[('fixed_price', 'fixed price'), ('percentage_discount', 'percentage discount'), ('fixed_discount', 'fixed discount')], max_length=30, verbose_name='discount type')),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='discount value')),
                ('minimal_amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='minimum check amount to apply')),
                ('is_active', models.BooleanField(default=True, verbose_name='promo code is active')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='codes', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('products', models.ManyToManyField(blank=True, related_name='promos', through='promo.ProductPromoCode', to='promo.product', verbose_name='promo assign to products')),
            ],
            options={
                'verbose_name': 'promo',
                'verbose_name_plural': 'promos',
                'db_table': 'content"."promo',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='productpromocode',
            name='promo_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='promo.promocode'),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('applied_user_id', models.UUIDField(verbose_name='code is activated by (UUID id)')),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='amount of the applied discount')),
                ('billing_info', models.TextField(blank=True, null=True, verbose_name='info from billing service')),
                ('promocode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='history', to='promo.promocode', verbose_name='activated promo')),
            ],
            options={
                'verbose_name': 'activation log',
                'verbose_name_plural': 'activations log',
                'db_table': 'content"."history',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='bulkpromocreate',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='promos_bulk', through='promo.ProductPromoCode', to='promo.product', verbose_name='promo assign to products'),
        ),
        migrations.AddConstraint(
            model_name='productpromocode',
            constraint=models.UniqueConstraint(fields=('product', 'promo_code'), name='UniqProductPerPromo'),
        ),
        migrations.AddConstraint(
            model_name='productpromocode',
            constraint=models.UniqueConstraint(fields=('product', 'bulk'), name='UniqProductPerBulk'),
        ),
        migrations.AddConstraint(
            model_name='productpromocode',
            constraint=models.CheckConstraint(check=models.Q(('promo_code__isnull', False), ('bulk__isnull', False), _connector='OR'), name='not_both_null'),
        ),
    ]