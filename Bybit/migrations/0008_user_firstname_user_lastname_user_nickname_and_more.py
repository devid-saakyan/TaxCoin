# Generated by Django 5.1.1 on 2024-12-22 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bybit', '0007_alter_referral_referred_user_alter_referral_referrer'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firstname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='photo_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]