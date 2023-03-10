# Generated by Django 4.1.7 on 2023-03-06 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0004_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Описание краткое'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Стоимость полная'),
        ),
    ]