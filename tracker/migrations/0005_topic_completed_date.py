# Generated by Django 5.1.2 on 2024-10-25 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_alter_topic_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='completed_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
