# Generated by Django 3.1.7 on 2021-06-21 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20210622_0120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='isFarmProduct',
        ),
    ]
