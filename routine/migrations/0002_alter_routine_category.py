# Generated by Django 4.1.1 on 2022-09-16 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='category',
            field=models.CharField(choices=[('기상관련', 'MIRACLE'), ('숙제관련', 'CATEGORY')], max_length=128),
        ),
    ]
