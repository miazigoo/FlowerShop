# Generated by Django 3.2 on 2023-08-18 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0006_auto_20230819_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='productcategory',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='flowers.product', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='pricecategory',
            name='from_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='От:'),
        ),
        migrations.AlterField(
            model_name='pricecategory',
            name='up_to_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='До:'),
        ),
    ]
