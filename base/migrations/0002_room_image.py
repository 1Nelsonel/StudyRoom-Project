# Generated by Django 4.0.5 on 2022-08-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(null=True, upload_to='image'),
        ),
    ]