# Generated by Django 4.2.4 on 2023-08-19 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_dataset_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relevant',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='result',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
