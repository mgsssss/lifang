# Generated by Django 4.1.4 on 2023-01-18 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifanguser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifanguser',
            name='level',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user')], max_length=64, verbose_name='등급'),
        ),
    ]
