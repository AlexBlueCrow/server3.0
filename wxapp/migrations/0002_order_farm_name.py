# Generated by Django 2.2.5 on 2020-08-13 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='farm_name',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]