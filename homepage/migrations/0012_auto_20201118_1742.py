# Generated by Django 2.2.5 on 2020-11-18 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0034_auto_20201117_1654'),
        ('homepage', '0011_auto_20201117_1748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tcvideo',
            old_name='farmuser',
            new_name='AdminUser',
        ),
        migrations.AddField(
            model_name='adminuser',
            name='farminfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='wxapp.FarmUser'),
        ),
    ]
