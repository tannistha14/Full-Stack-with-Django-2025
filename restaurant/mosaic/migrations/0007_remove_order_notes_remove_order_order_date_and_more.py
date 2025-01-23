# Generated by Django 5.1.5 on 2025-01-23 16:15

import django.utils.timezone
from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('mosaic', '0006_remove_menuitem_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
