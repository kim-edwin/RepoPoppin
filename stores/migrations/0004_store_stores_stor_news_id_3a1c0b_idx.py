# Generated by Django 5.0.1 on 2024-03-16 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_alter_store_frontlat_alter_store_frontlon'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['news_id'], name='stores_stor_news_id_3a1c0b_idx'),
        ),
    ]
