# Generated by Django 2.2.5 on 2020-12-30 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='imageUrl',
            field=models.CharField(blank=True, default='', max_length=128, null=True),
        ),
    ]
