# Generated by Django 3.1.7 on 2021-06-21 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20210611_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='harvestTime',
        ),
        migrations.RemoveField(
            model_name='product',
            name='productType',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='farmerPicture',
            field=models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to=''),
        ),
    ]