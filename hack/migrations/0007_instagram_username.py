# Generated by Django 4.2.9 on 2024-02-03 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack', '0006_instagram'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagram',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]