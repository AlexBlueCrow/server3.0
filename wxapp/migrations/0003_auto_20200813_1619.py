# Generated by Django 2.2.5 on 2020-08-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0002_order_farm_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.IntegerField(choices=[(0, 'inactive'), (1, 'active'), (2, 'expire')], default=0),
        ),
    ]
