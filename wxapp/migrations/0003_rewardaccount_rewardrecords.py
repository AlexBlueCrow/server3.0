# Generated by Django 2.2.5 on 2021-01-08 14:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0002_auto_20201230_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='RewardAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wxapp.AppUser')),
            ],
        ),
        migrations.CreateModel(
            name='RewardRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.IntegerField(default=0)),
                ('msg', models.CharField(blank=True, default='', max_length=128)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wxapp.RewardAccount')),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wxapp.AppUser')),
            ],
        ),
    ]
