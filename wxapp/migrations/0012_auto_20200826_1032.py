# Generated by Django 2.2.5 on 2020-08-26 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0011_auto_20200826_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prepay_order',
            name='genre',
            field=models.CharField(choices=[('adopt', 'adopt'), ('sell', 'sell')], default='sell', max_length=10),
        ),
    ]