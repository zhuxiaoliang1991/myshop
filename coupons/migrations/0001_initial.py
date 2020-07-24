# Generated by Django 2.0.5 on 2020-07-23 12:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='优惠券卡号')),
                ('valid_from', models.DateTimeField(verbose_name='起始有效期')),
                ('valid_to', models.DateTimeField(verbose_name='终止有效期')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='折扣')),
                ('active', models.BooleanField(verbose_name='是否有效')),
            ],
            options={
                'verbose_name': '优惠券',
                'verbose_name_plural': '优惠券',
            },
        ),
    ]
