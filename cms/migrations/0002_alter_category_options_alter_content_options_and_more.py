# Generated by Django 5.1.5 on 2025-01-21 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'verbose_name_plural': 'Contents'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
