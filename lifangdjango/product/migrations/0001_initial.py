# Generated by Django 4.1.4 on 2023-01-18 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lifanguser', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('fake_num', models.IntegerField(verbose_name='가품발견수')),
                ('site_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lifanguser.company')),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(max_length=255, upload_to='')),
                ('brand_name', models.CharField(default='', max_length=256, null=True, verbose_name='브랜드명')),
                ('name', models.CharField(default='', max_length=256, null=True, verbose_name='상품명')),
                ('price', models.IntegerField(verbose_name='상품가격')),
                ('url', models.URLField(max_length=255)),
                ('descrtiption', models.TextField(verbose_name='상품설명')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.project')),
            ],
            options={
                'verbose_name': '기업목록',
                'verbose_name_plural': '기업목록',
                'db_table': 'product',
            },
        ),
    ]
