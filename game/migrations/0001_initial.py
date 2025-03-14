# Generated by Django 5.1.7 on 2025-03-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WordleGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_word', models.CharField(max_length=5)),
                ('attempts', models.JSONField(default=list)),
                ('status', models.CharField(choices=[('IN_PROGRESS', 'In Progress'), ('WON', 'Won'), ('LOST', 'Lost')], default='IN_PROGRESS', max_length=20)),
                ('max_attempts', models.IntegerField(default=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=5, unique=True)),
            ],
        ),
    ]
