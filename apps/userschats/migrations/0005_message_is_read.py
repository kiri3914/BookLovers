# Generated by Django 4.2.5 on 2023-09-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userschats', '0004_alter_message_book_shared'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]