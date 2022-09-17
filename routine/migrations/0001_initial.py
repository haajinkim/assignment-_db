# Generated by Django 4.1.1 on 2022-09-17 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('category', models.CharField(choices=[('HOMEWORK', 'HOMEWORK'), ('MIRACLE', 'MIRACLE')], max_length=128)),
                ('goal', models.CharField(max_length=128)),
                ('is_alarm', models.BooleanField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoutineResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('TRY', 'TRY'), ('NOT', 'NOT'), ('DONE', 'DONE')], default='NOT', max_length=128)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('routine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routine.routine')),
            ],
        ),
        migrations.CreateModel(
            name='RoutineDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('routine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routine.routine')),
            ],
        ),
    ]
