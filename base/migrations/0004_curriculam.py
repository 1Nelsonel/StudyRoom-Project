# Generated by Django 4.0.5 on 2022-08-22 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_topic_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(blank=True, null=True, upload_to='files')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.room')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
