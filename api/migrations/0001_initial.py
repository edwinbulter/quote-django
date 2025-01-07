# Generated by Django 5.1.4 on 2025-01-06 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_text', models.CharField(max_length=1000)),
                ('author', models.CharField(max_length=100)),
                ('likes', models.IntegerField()),
            ],
        ),
    ]
