# Generated by Django 4.2.3 on 2023-10-24 05:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("emo_core", "0002_tempregister"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="advicedata",
            name="effectiveness",
        ),
        migrations.RemoveField(
            model_name="advicedata",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="emotiondata",
            name="updated_at",
        ),
    ]
