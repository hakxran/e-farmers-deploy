# Generated by Django 3.1.7 on 2021-05-17 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_remove_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='farmerPoint',
            field=models.FloatField(default=0),
        ),
    ]