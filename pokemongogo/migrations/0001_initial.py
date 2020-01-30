# Generated by Django 3.0.2 on 2020-01-30 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CounterInfo',
            fields=[
                ('cName', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('cCategory', models.CharField(max_length=255)),
                ('cUrl', models.URLField(unique=True)),
            ],
        ),
    ]
