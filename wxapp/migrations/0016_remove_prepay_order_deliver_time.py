# Generated by Django 2.2.5 on 2020-08-26 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0015_order_imageurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prepay_order',
            name='deliver_time',
        ),
    ]
