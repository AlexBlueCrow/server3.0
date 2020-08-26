# Generated by Django 2.2.5 on 2020-08-26 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0010_auto_20200826_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='nickname',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='post_sign',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AddField(
            model_name='prepay_order',
            name='genre',
            field=models.CharField(choices=[('adopt', 'adopt'), ('sell', 'sell')], default='sell', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prepay_order',
            name='nickname',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='prepay_order',
            name='post_sign',
            field=models.CharField(default='', max_length=40),
        ),
    ]
