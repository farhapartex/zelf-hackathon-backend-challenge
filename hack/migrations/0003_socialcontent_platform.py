# Generated by Django 4.2.9 on 2024-02-03 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack', '0002_author_username_alter_author_data_alter_author_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialcontent',
            name='platform',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]