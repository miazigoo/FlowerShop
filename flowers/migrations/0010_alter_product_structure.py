# Generated by Django 3.2 on 2023-08-19 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0009_auto_20230819_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='structure',
            field=models.TextField(blank=True, null=True, verbose_name='Состав'),
        ),
    ]
