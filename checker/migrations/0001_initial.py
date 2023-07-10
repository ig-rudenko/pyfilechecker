# Generated by Django 4.2.3 on 2023-07-10 19:02

import checker.models
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
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mod_time', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=checker.models.upload_to)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'files',
            },
        ),
        migrations.CreateModel(
            name='CheckStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NCK', 'Не проверенный'), ('SCS', 'Нет ошибок'), ('ERR', 'Если ошибки'), ('FAL', 'Ошибка анализа')], default='NCK', max_length=3)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField(default='')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='checker.file')),
            ],
            options={
                'db_table': 'checks',
            },
        ),
    ]