# Generated by Django 5.1.4 on 2025-02-14 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='content',
        ),
        migrations.AddField(
            model_name='message',
            name='_content',
            field=models.TextField(db_column='content', default=''),
        ),
    ]
