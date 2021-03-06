# Generated by Django 2.2.5 on 2021-01-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0003_rewardaccount_rewardrecords'),
    ]

    operations = [
        migrations.AddField(
            model_name='prepay_order',
            name='reward',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='prepay_order',
            name='shareId',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='prepay_order',
            name='shareReward',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
