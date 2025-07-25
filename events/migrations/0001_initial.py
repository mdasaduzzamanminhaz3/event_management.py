# Generated by Django 5.2.3 on 2025-07-24 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=250)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.TextField(max_length=150)),
                ('asset', models.ImageField(blank=True, default='event_asset/default_img.jpg', null=True, upload_to='event_asset')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.category')),
            ],
        ),
    ]
