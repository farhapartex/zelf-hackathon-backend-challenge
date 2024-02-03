# Generated by Django 4.2.9 on 2024-02-03 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack', '0004_author_is_fetched'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialcontent',
            name='comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='socialcontent',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='socialcontent',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='socialcontent',
            name='media_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='socialcontent',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
