# Generated by Django 4.0.7 on 2022-09-06 16:11

from django.db import migrations, models
import watchlist.models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0006_watchlist_remove_review_watch_delete_watch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='image',
            field=models.ImageField(null=True, upload_to=watchlist.models.watchlist_file_upload_path),
        ),
    ]
